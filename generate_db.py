import pandas as pd

RAW_DATASET = "raw_dataset/"
PROCESSED_DATASET = "processed_dataset/"
ACTORS = "name.basics.tsv"
MOVIES = "title.basics.tsv"
MOVIES_ACTORS = "title.principals.tsv"
NUM_ROWS = 10000


def load_and_save_actors() -> None:
    actors: pd.DataFrame = pd.read_csv(
        RAW_DATASET + ACTORS, sep="\t", low_memory=True, nrows=NUM_ROWS
    )[["nconst", "primaryName"]].drop_duplicates()
    actors.to_csv(PROCESSED_DATASET + ACTORS, sep="\t")


def load_and_save_movies() -> None:
    movies: pd.DataFrame = pd.read_csv(
        RAW_DATASET + MOVIES, sep="\t", low_memory=True, nrows=NUM_ROWS
    ).drop_duplicates()
    movies = movies.loc[movies["titleType"] == "movie", ["tconst", "primaryTitle"]]
    movies.to_csv(PROCESSED_DATASET + MOVIES, sep="\t")


def load_and_save_movies_actors() -> None:
    movies_actors: pd.DataFrame = pd.read_csv(
        RAW_DATASET + MOVIES_ACTORS, sep="\t", low_memory=True, nrows=NUM_ROWS
    )[["tconst", "nconst"]].drop_duplicates()
    movies_actors.to_csv(PROCESSED_DATASET + MOVIES_ACTORS, sep="\t")

def generate_db() -> None:
    load_and_save_actors()
    load_and_save_movies()
    load_and_save_movies_actors()

if __name__ == "__main__":
    generate_db()