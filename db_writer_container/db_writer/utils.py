from typing import Tuple
import os


def get_auth_from_env() -> Tuple[str, str]:
    """
    Gets the username and password for the db
    Raises:
        KeyError: If no env var for this exists, raise an error.

    Returns:
        Tuple[str]: (username, password)
    """
    from db_writer.consts import AUTH_ENV

    neo4j_auth = os.getenv(AUTH_ENV)
    if neo4j_auth is None:
        raise KeyError("No auth env var is defined!")
    else:
        username, password = neo4j_auth.split("/", 1)
        return username, password
