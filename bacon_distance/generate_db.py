import pandas as pd

from consts import (
    ACTORS,
    MOVIES,
    MOVIES_ACTORS,
    NUM_ROWS,
    PROCESSED_DATASET,
    RAW_DATASET,
    SKIP_ROWS,
)


def load_and_save_actors() -> None:
    actors: pd.DataFrame = pd.read_csv(
        RAW_DATASET.joinpath(ACTORS), sep="\t", low_memory=True, nrows=NUM_ROWS
    )[["nconst", "primaryName"]].drop_duplicates()
    actors.rename(
        columns={"nconst": "actor_id", "primaryName": "actor_name"}, inplace=True
    )
    actors.to_csv(PROCESSED_DATASET.joinpath(ACTORS), sep="\t")
    print("Finished actors")


def load_and_save_movies() -> None:
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
    load_and_save_actors()
    load_and_save_movies()
    load_and_save_movies_actors()


if __name__ == "__main__":
    generate_db()
