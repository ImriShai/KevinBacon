from pathlib import Path

RAW_DATASET = Path("raw_dataset/")
PROCESSED_DATASET = Path("processed_dataset/")
ACTORS = Path("name.basics.tsv")
MOVIES = Path("title.basics.tsv")
MOVIES_ACTORS = Path("title.principals.tsv")
NUM_ROWS = 100000 # Enough to generate dataset with a movie with Kevin Bacon
SKIP_ROWS = 1000000 #
KEVIN_BACON_ID = "nm0000102"
