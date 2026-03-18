from bacon_server.utils import get_auth_from_env

KEVIN_BACON_ID = "nm0000102"
URI = "neo4j://service-neo4j"  # Host name can't start with neo4j otherwise collides with neo4j config
AUTH_ENV = "NEO4J_AUTH"
DATABASE = "neo4j"
AUTH = get_auth_from_env()
PORT = 5000
RABBIT_QUEUE = "new_movies"
RABBIT_HOST = "rabbitmq"
