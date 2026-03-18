from pathlib import Path

from utils import get_auth_from_env

RAW_DATASET = Path("/raw_dataset/")
PROCESSED_DATASET = Path("/processed_dataset/")
ACTORS = Path("name.basics.tsv")
MOVIES = Path("title.basics.tsv")
MOVIES_ACTORS = Path("title.principals.tsv")
NUM_ROWS = 100000  # Enough to generate dataset with a movie with Kevin Bacon
SKIP_ROWS = 1000000  # same reason
KEVIN_BACON_ID = "nm0000102"
TEST_ID = "nm0000720"
REQUIRED_RESULT = 2
URI = "neo4j://service-neo4j"  # Host name can't start with neo4j otherwise collides with neo4j config

AUTH_ENV = "NEO4J_AUTH"
DATABASE = "neo4j"
AUTH = get_auth_from_env()
