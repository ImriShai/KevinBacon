# KevinBacon
## Project Overview

The goal of this project is to allow users to calculate the Bacon distance of a chosen actor using data from the IMDb dataset.

The Bacon distance measures how closely an actor is connected to Kevin Bacon through shared movie appearances. If an actor has appeared in a film with Kevin Bacon, their Bacon number is 1. If they appeared with someone who appeared with Kevin Bacon, their Bacon number is 2, and so on.

To efficiently compute these relationships, this project uses the Neo4j graph database. A graph database is particularly well suited for this problem because the core operation required is finding the **shortest path** between nodes.
