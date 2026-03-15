from math import ceil, inf

import pandas as pd
from typing import Tuple
import networkx as nx

from consts import ACTORS, KEVIN_BACON_ID, MOVIES, MOVIES_ACTORS, PROCESSED_DATASET


def init_server() -> Tuple[pd.DataFrame, nx.Graph]:
    """
    Init the data frames and the graphs
    Returns:
        Tuple[pd.DataFrame, nx.Graph]: The actors df and the initalized graph.
    """
    actors, movies, movies_actors = load_data(
        PROCESSED_DATASET.joinpath(ACTORS),
        PROCESSED_DATASET.joinpath(MOVIES),
        PROCESSED_DATASET.joinpath(MOVIES_ACTORS),
    )
    g = nx.Graph()
    add_actors(g, actors)
    add_movies(g, movies)
    add_edges(g, movies_actors)
    return actors, g


def calculate_bacon_distance(g: nx.Graph, source: str) -> float:
    """
    Given the name as source and the created graph, computes the distance to Kevin Bacon.
    Args:
        g (nx.Graph): The graph to search on.
        source (str): The source to search from.

    Returns:
        float: The distance from source to Kevin Baccon. If no path return inf.
    """
    try:
        path = list(nx.shortest_path(g, source, KEVIN_BACON_ID))
        return ceil((len(path) / 2)) - 1
    except nx.NetworkXNoPath:
        return inf


def get_actor_id_from_name(actors: pd.DataFrame, name: str) -> str:
    """
    Given a name to serach returns the id of the actor from the actors data frame.
    Args:
        name (str): The actors name to search
        actors (pd.DataFrame): The actors data frame

    Raises:
        ValueError: If no actor with this name exist, raises value error.

    Returns:
        str: The founded id of the actor
    """
    actor_id: pd.DataFrame = actors.loc[actors["actor_name"] == name, ["actor_id"]]
    if actor_id.empty:
        raise ValueError("There is no actor with this name!")
    else:
        return list(actor_id["actor_id"].head(1))[0]


def add_actors(g: nx.Graph, actors: pd.DataFrame) -> None:
    """
    Given a graph and the actors df, inserts the actors as nodes in the graph.
    Args:
        g (nx.Graph): The graph
        actors (pd.DataFrame): The actors df
    """
    for _, actor in actors.iterrows():
        g.add_node(actor["actor_id"], name=actor["actor_name"])


def add_movies(g: nx.Graph, movies: pd.DataFrame) -> None:
    """
    Given a graph and the movies df, inserts the movies as nodes in the graph.
    Args:
        g (nx.Graph): The graph
        movies (pd.DataFrame): The movies df
    """
    for _, movie in movies.iterrows():
        g.add_node(movie["movie_id"], title=movie["movie_name"])


def add_edges(g: nx.Graph, movies_actors: pd.DataFrame) -> None:
    """
    Given a graph and the movies_actors df, creates an edge for each entry in the df
    from actor node to movie node,
    Args:
        g (nx.Graph): The graph
        movies_actors (pd.DataFrame): The df containing the realtions.
    """
    for _, movie_actor in movies_actors.iterrows():
        g.add_edge(movie_actor["movie_id"], movie_actor["actor_id"])


def load_data(actors: str, movies: str, movies_actors: str) -> Tuple[pd.DataFrame]:
    """
    Given tha paths of the dataset, returns a dataframe for each one
    Args:
        actors (str): The actors dataset path
        movies (str): The movies dataset path
        movies_actors (str): The movies_actors dataset path

    Returns:
        Tuple[pd.DataFrame]: Dataframes of the data
    """
    actors_df = pd.read_csv(actors, sep="\t")
    movies_df = pd.read_csv(movies, sep="\t")
    movies_actors_df = pd.read_csv(movies_actors, sep="\t")
    return actors_df, movies_df, movies_actors_df
