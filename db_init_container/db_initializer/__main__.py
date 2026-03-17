from math import ceil
from pathlib import Path
from typing import Tuple

import pandas as pd
from neo4j import GraphDatabase, Driver
from consts import *


def load_and_save_actors() -> None:
    """
    Loads the unproccesed actors data proccess it and saves the result.
    """
    actors: pd.DataFrame = pd.read_csv(
        RAW_DATASET.joinpath(ACTORS), sep="\t", low_memory=True, nrows=NUM_ROWS
    )[["nconst", "primaryName"]].drop_duplicates()
    actors.rename(
        columns={"nconst": "actor_id", "primaryName": "actor_name"}, inplace=True
    )
    actors.to_csv(PROCESSED_DATASET.joinpath(ACTORS), sep="\t")
    print("Finished actors")


def load_and_save_movies() -> None:
    """
    Loads the unproccesed movies data proccess it and saves the result.
    """
    movies: pd.DataFrame = pd.read_csv(
        RAW_DATASET.joinpath(MOVIES), sep="\t", low_memory=True, nrows=NUM_ROWS
    ).drop_duplicates()
    movies = movies.loc[movies["titleType"] == "movie", ["tconst", "primaryTitle"]]
    movies.rename(
        columns={"tconst": "movie_id", "primaryTitle": "movie_name"}, inplace=True
    )
    movies.to_csv(PROCESSED_DATASET.joinpath(MOVIES), sep="\t")
    print("Finished movies")


def load_and_save_movies_actors() -> None:
    """
    Loads the unproccesed movies_actors data proccess it and saves the result.
    """
    movies_actors: pd.DataFrame = pd.read_csv(
        RAW_DATASET.joinpath(MOVIES_ACTORS),
        sep="\t",
        low_memory=True,
        nrows=NUM_ROWS,
        skiprows=[i for i in range(1, SKIP_ROWS)],
    )[["tconst", "nconst"]].drop_duplicates()
    movies_actors.rename(
        columns={"nconst": "actor_id", "tconst": "movie_id"}, inplace=True
    )

    movies_actors.to_csv(PROCESSED_DATASET.joinpath(MOVIES_ACTORS), sep="\t")
    print("Finished movies_actors")


def generate_db() -> None:
    """
    Loads, proccess and saves to db all the data.
    """
    load_and_save_actors()
    load_and_save_movies()
    load_and_save_movies_actors()
    actors, movies, movies_actors = load_data(ACTORS, MOVIES, MOVIES_ACTORS)
    with GraphDatabase.driver(URI, auth=AUTH) as connection:
        connection.verify_connectivity()
        add_actors(connection, actors)
        add_movies(connection, movies)
        create_indexes(connection)
        add_edges(connection, movies_actors)


def add_actors(connection: Driver, actors: pd.DataFrame) -> None:
    """
    Given a connection to the db and the actors df, inserts the actors as nodes in the graph.
    Args:
        connection (Driver): The db connection
        actors (pd.DataFrame): The actors df
    """
    actors_list = actors.to_dict("records")

    query = """
            UNWIND $actors_list as actor
            CREATE (a:Actor {name: actor.actor_name, id: actor.actor_id})
            """
    with connection.session(database=DATABASE) as session:
        summary = session.execute_write(
            lambda tx: tx.run(query, actors_list=actors_list).consume()
        )
        print(f"Created {summary.counters.nodes_created} actors nodes.")


def add_movies(connection: Driver, movies: pd.DataFrame) -> None:
    """
    Given a connection to the db and the movies df, inserts the actors as nodes in the graph.
    Args:
        connection (Driver): The db connection
        movies (pd.DataFrame): The movies df
    """
    movies_list = movies.to_dict("records")

    query = """
            UNWIND $movies_list AS movie
            CREATE (m:Movie {name: movie.movie_name, id: movie.movie_id})
            """
    with connection.session(database=DATABASE) as session:
        summary = session.execute_write(
            lambda tx: tx.run(query, movies_list=movies_list).consume()
        )
        print(f"Created {summary.counters.nodes_created} movies nodes.")


def create_indexes(connection: Driver) -> None:
    """
    Creates indexes on Actor.id,name and Movie.id,name to speed up relationship creation.
    """
    queries = [
        "CREATE INDEX actor_id_index IF NOT EXISTS FOR (a:Actor) ON (a.id)",
        "CREATE INDEX actor_name_index IF NOT EXISTS FOR (a:Actor) ON (a.name)",
        "CREATE INDEX movie_id_index IF NOT EXISTS FOR (m:Movie) ON (m.id)",
        "CREATE INDEX movie_name_index IF NOT EXISTS FOR (m:Movie) ON (m.name)",
    ]

    with connection.session(database=DATABASE) as session:
        for query in queries:
            session.run(query)
            print(f"Executed: {query}")

    print("Indexes created (or already existed).")


def add_edges(connection: Driver, movies_actors: pd.DataFrame) -> None:
    """
    Given a connection to the db and the movies_actors df, inserts the actors as nodes in the graph.
    Args:
        connection (Driver): The db connection
        movies_actors (pd.DataFrame): The movies_actors df
    """
    movies_actors_list = movies_actors.to_dict("records")

    query = """
            UNWIND $rows AS row
            CALL (row) {
                MATCH (a:Actor {id: row.actor_id})
                MATCH (m:Movie {id: row.movie_id})
                MERGE (a)-[:PLAYS_IN]->(m)
            } IN TRANSACTIONS OF 1000 ROWS
        """
    with connection.session(database=DATABASE) as session:
        summary = session.run(query, rows=movies_actors_list).consume()
        print(
            f"Created {summary.counters.relationships_created} PLAYED_IN relationship."
        )


def load_data(
    actors: Path, movies: Path, movies_actors: Path, base_dir=PROCESSED_DATASET
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Given tha paths of the dataset, returns a dataframe for each one
    Args:
        actors (Path): The actors dataset path
        movies (Path): The movies dataset path
        movies_actors (Path): The movies_actors dataset path

    Returns:
        Tuple[pd.DataFrame]: Dataframes of the data
    """
    actors_df = pd.read_csv(base_dir.joinpath(actors), sep="\t")
    movies_df = pd.read_csv(base_dir.joinpath(movies), sep="\t")
    movies_actors_df = pd.read_csv(base_dir.joinpath(movies_actors), sep="\t")
    return actors_df, movies_df, movies_actors_df


def test_neo() -> bool:
    """
    This method checks if the db is initialized by testing the bacon distance of Jim Abrahams.

    Returns:
        bool: True if the distance is as expected, otherwise False.
    """
    connection = GraphDatabase.driver(URI, auth=AUTH)
    with connection.session(database=DATABASE) as session:
        test_query = """
                    MATCH (source:Actor {id: $kevin_id}), (target:Actor {id: $test_id})
                    MATCH p = shortestPath((source)-[*]-(target))
                    RETURN length(p) AS distance  
                    """
        result = session.execute_read(
            lambda tx: tx.run(
                test_query, kevin_id=KEVIN_BACON_ID, test_id=TEST_ID
            ).single()
        )
        if result and result["distance"] / 2 == REQUIRED_RESULT:
            return True
        else:
            return False


if __name__ == "__main__":
    if not test_neo():
        print("db isn't initialzied. Starting generate_db")
        generate_db()
    else:
        print("db already initialized")
