from math import inf
from typing import Optional, Tuple
from bacon_server.utils import calculate_bacon_distance
from flask import Flask, request
from flask_cors import CORS
from http import HTTPStatus
from neo4j import Driver, GraphDatabase
import pika
from pika.adapters.blocking_connection import BlockingChannel, BlockingConnection
from pika.spec import Basic, BasicProperties
from bacon_server.consts import AUTH, PORT, RABBIT_HOST, RABBIT_QUEUE, URI

RESPONSE = Tuple[str, HTTPStatus]


app = Flask("Bacon Distance Calculator")
CORS(app)

connection: Driver
queue_connection: BlockingConnection
queue_channel: BlockingChannel


def start_server() -> None:
    """
    Calls the server initalizer then runs it.
    """
    global connection, queue_connection, queue_channel
    try:
        with GraphDatabase.driver(URI, auth=AUTH) as connection:
            queue_connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBIT_HOST)
            )
            queue_channel = queue_connection.channel()
            queue_channel.queue_declare(queue=RABBIT_QUEUE, durable=True)
            app.run("0.0.0.0", PORT, debug=True)
    finally:
        queue_channel.close()
        queue_connection.close()


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
    global connection
    if connection is None:
        return "An error has accured", HTTPStatus.INTERNAL_SERVER_ERROR
    actor_name = request.get_json()["name"]
    if actor_name == "Kevin Bacon":
        distance: Optional[float] = 0.0
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


@app.post("/new-movie")
def send_new_movie() -> RESPONSE:
    """
    A callback for when the /new-movie endpoint recives a request.
    It sends the new-movies queue a request for new movie.
    Returns:
        RESPONSE: The str response and a status code. OK if sent succesfully to queue.
    """
    global queue_channel
    data = request.data
    try:
        queue_channel.basic_publish(
            exchange="",
            routing_key=RABBIT_QUEUE,
            body=data,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent,
            ),
        )
        return "Added to database", HTTPStatus.OK
    except Exception as e:
        return f"An error has accured: {e}", HTTPStatus.INTERNAL_SERVER_ERROR
