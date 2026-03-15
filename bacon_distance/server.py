from math import inf
from typing import Optional, Tuple
from bacon_distance.bacon_distance import (
    calculate_bacon_distance,
    get_actor_id_from_name,
    init_server,
)
from flask import Flask, request
from flask_cors import CORS
from http import HTTPStatus
import pandas as pd
import networkx as nx


RESPONSE = Tuple[str, HTTPStatus]


app = Flask("Bacon Distance Calculator")
CORS(app)

actors: Optional[pd.DataFrame] = None
g: Optional[nx.Graph] = None


def start_server() -> None:
    """
    Calls the server initalizer then runs it.
    """
    global actors, g
    actors, g = init_server()
    app.run("0.0.0.0", 5555, debug=True)


@app.get("/ping")
def health_check() -> str:
    """
    A health check for the server
    """
    return "pong"


@app.post("/calculate")
def calculate_distance() -> RESPONSE:
    actor_name = request.get_json()["name"]
    try:
        actor_id = get_actor_id_from_name(actors, actor_name)
    except ValueError:
        return "There is no actor with this name!", HTTPStatus.BAD_REQUEST
    distance = calculate_bacon_distance(g, actor_id)
    if distance == inf:
        return (
            f"There is no path from {actor_name} to Kevin Bacon!",
            HTTPStatus.BAD_REQUEST,
        )
    else:
        return (
            f"The distacne from Kevin Bacon to {actor_name} is: {distance}",
            HTTPStatus.OK,
        )
