from db_writer.utils import get_auth_from_env

URI = "neo4j://neo4j"
AUTH_ENV = "NEO4J_AUTH"
DATABASE = "neo4j"
RABBIT_QUEUE = "new_movies"
RABBIT_HOST = "rabbitmq"
AUTH = get_auth_from_env()
