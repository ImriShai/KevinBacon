from math import inf
from typing import Optional, Tuple
from bacon_server.utils import calculate_bacon_distance
from flask import Flask, request
from flask_cors import CORS
from http import HTTPStatus
from neo4j import Driver, GraphDatabase

from bacon_server.consts import AUTH, PORT, URI


RESPONSE = Tuple[str, HTTPStatus]


app = Flask("Bacon Distance Calculator")
CORS(app)

connection: Optional[Driver]


def start_server() -> None:
    """
    Calls the server initalizer then runs it.
    """
    global connection
    with GraphDatabase.driver(URI, auth=AUTH) as connection:
        app.run("0.0.0.0", PORT, debug=True)


@app.get("/ping")
def health_check() -> str:
    """
    A health check for the server
    """
    return "pong"


@app.post("/calculate")
def calculate_distance() -> RESPONSE:
    """
    A callback for when the /calculate endpoint recives a request.
    It query the db for the bacon distance
    Returns:
        RESPONSE: The str response and a status code. The distance if a valid name.
    """
    actor_name = request.get_json()["name"]
    if actor_name == "Kevin Bacon":
        distance = 0
    else:
        distance = calculate_bacon_distance(connection, actor_name)
    if distance is None:
        return (
            f"There is no node with the name {actor_name}!",
            HTTPStatus.BAD_REQUEST,
        )
    if distance == inf:
        return (
            f"There is no path from {actor_name} to Kevin Bacon!",
            HTTPStatus.BAD_REQUEST,
        )
    else:
        return (
            f"The distacne from Kevin Bacon to {actor_name} is: {int(distance)}",
            HTTPStatus.OK,
        )
