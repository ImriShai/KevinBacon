from typing import Tuple
import os
from math import inf
from neo4j import Driver
from typing import Optional


def get_auth_from_env() -> Tuple[str, str]:
    """
    Gets the username and password for the db
    Raises:
        KeyError: If no env var for this exists, raise an error.

    Returns:
        Tuple[str]: (username, password)
    """
    from consts import AUTH_ENV

    neo4j_auth = os.getenv(AUTH_ENV)
    if neo4j_auth is None:
        raise KeyError("No auth env var is defined!")
    else:
        username, password = neo4j_auth.split("/", 1)
        return username, password


def calculate_bacon_distance(connection: Driver, source: str) -> Optional[float]:
    """
    Given the name as source and a connection to the db, computes the distance to Kevin Bacon.
    Args:
        source (str): The source to search from.
        connection (Driver): The connection to the neo4j db
    Returns:
        float: The distance from source to Kevin Baccon. If no path return inf.
    """
    from consts import DATABASE, KEVIN_BACON_ID

    try:
        with connection.session(database=DATABASE) as session:
            query = """
                        MATCH (source:Actor {id: $kevin_id}), (target:Actor {name: $actor_name})
                        MATCH p = shortestPath((source)-[*]-(target))
                        RETURN length(p) AS distance  
                        """
            result = session.execute_read(
                lambda tx: tx.run(
                    query, actor_name=source, kevin_id=KEVIN_BACON_ID
                ).single()
            )
            if result is not None:
                return result.get("distance", inf) / 2
            return None  # Happens only when the source is not defined well, meaning no node with this name.

    except Exception as e:
        print(e)
        return inf
