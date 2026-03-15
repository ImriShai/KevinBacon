import pandas as pd
from pathlib import Path

RAW_DATASET = Path("raw_dataset/")
PROCESSED_DATASET = Path("processed_dataset/")
ACTORS = Path("name.basics.tsv")
MOVIES = Path("title.basics.tsv")
MOVIES_ACTORS = Path("title.principals.tsv")
NUM_ROWS = 10000


def load_and_save_actors() -> None:
    actors: pd.DataFrame = pd.read_csv(
        RAW_DATASET.joinpath(ACTORS), sep="\t", low_memory=True, nrows=NUM_ROWS
    )[["nconst", "primaryName"]].drop_duplicates()
    actors.to_csv(PROCESSED_DATASET.joinpath(ACTORS), sep="\t")


def load_and_save_movies() -> None:
    movies: pd.DataFrame = pd.read_csv(
        RAW_DATASET.joinpath(MOVIES), sep="\t", low_memory=True, nrows=NUM_ROWS
    ).drop_duplicates()
    movies = movies.loc[movies["titleType"] == "movie", ["tconst", "primaryTitle"]]
    movies.to_csv(PROCESSED_DATASET.joinpath(MOVIES), sep="\t")


def load_and_save_movies_actors() -> None:
    movies_actors: pd.DataFrame = pd.read_csv(
        RAW_DATASET.joinpath(MOVIES_ACTORS), sep="\t", low_memory=True, nrows=NUM_ROWS
    )[["tconst", "nconst"]].drop_duplicates()
    movies_actors.to_csv(PROCESSED_DATASET.joinpath(MOVIES_ACTORS), sep="\t")


def generate_db() -> None:
    load_and_save_actors()
    load_and_save_movies()
    load_and_save_movies_actors()


if __name__ == "__main__":
    generate_db()
