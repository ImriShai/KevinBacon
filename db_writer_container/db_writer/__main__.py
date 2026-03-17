from typing import List, TypedDict

import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties
from db_writer.consts import AUTH, DATABASE, RABBIT_QUEUE, URI
from db_writer.consts import RABBIT_HOST
import json
from neo4j import GraphDatabase, Driver

Actor = TypedDict(
    "Actor",
    {
        "id": str,
        "name": str,
    },
)
Movie = TypedDict(
    "Movie",
    {
        "id": str,
        "name": str,
    },
)
Payload = TypedDict("Payload", {"Movie": Movie, "Actors": List[Actor]})

connection: Driver


def callback(
    channel: BlockingChannel, method: Basic, properties: BasicProperties, body: bytes
) -> None:
    """
    A callback function to handle a read from the new_movies queue.
    Args:
        channel (BlockingChannel): The channel we read from
        method (Basic): The method in which the channel works.
        properties (BasicProperties): Basic properties of the message.
        body (bytes): The message itself.
    """
    try:
        data: Payload = json.loads(body)
        movie: Movie = data["Movie"]
        actors_list: List[Actor] = data["Actors"]
        print(
            f"Recived a new message from new_moveis queue with {movie}, {actors_list}"
        )
        create_new_movie(movie, actors_list)
        channel.basic_ack(delivery_tag=method.delivery_tag)
    except KeyError:
        print("The given data isn't in the correct format!")


def create_new_movie(movie: Movie, actors_list: List[Actor]) -> None:
    """
    Given a new movie and a list of actors that plays in this movie, Adds the movie to the db, and connects
    the actors to the movie.
    If the Actor already exist, it only connect it to movie, otherwise creates the actor as well.
    Args:
        movie (Movie): The movie in format of {id: movie_id, name: movie_name}
        actors_list (List[Actor]): The list of actors in a format of [{id: actor_id, name: actor_name}]
    """
    global connection
    if connection is None:
        return
    query = """
            UNWIND $actors_list AS actor
            MERGE (a:Actor {id: actor.id})
                ON CREATE SET a.name = actor.name
            MERGE (m:Movie {id: $movie_id})
                ON CREATE SET m.name = $movie_name
            MERGE (a)-[:PLAYS_IN]->(m)
            """
    with connection.session(database=DATABASE) as session:
        summary = session.execute_write(
            lambda tx: tx.run(
                query,
                actors_list=actors_list,
                movie_id=movie["id"],
                movie_name=movie["name"],
            ).consume()
        )
        print(
            f"created {summary.counters.nodes_created} new nodes of Movie and Actors."
        )
        print(f"Created {summary.counters.relationships_created} new connections.")


def main() -> None:
    """
    The main function running the db_writer.
    Runs forever while listening to new queue messages and writing them in the db.
    """
    global connection
    with GraphDatabase.driver(URI, auth=AUTH) as connection:
        rabbit_connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_HOST)
        )
        while True:
            try:
                channel: BlockingChannel = rabbit_connection.channel()
                channel.queue_declare(queue=RABBIT_QUEUE, durable=True)

                channel.basic_consume(queue=RABBIT_QUEUE, on_message_callback=callback)

                print("Listening to new movies queue")
                channel.start_consuming()
            finally:
                channel.close()
                connection.close()


if __name__ == "__main__":
    main()
