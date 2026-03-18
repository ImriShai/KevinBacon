from db_writer.utils import get_auth_from_env

URI = "neo4j://service-neo4j"  # Host name can't start with neo4j otherwise collides with neo4j config

AUTH_ENV = "NEO4J_AUTH"
DATABASE = "neo4j"
RABBIT_QUEUE = "new_movies"
RABBIT_HOST = "rabbitmq"
AUTH = get_auth_from_env()
