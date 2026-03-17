from setuptools import setup, find_packages

setup(
    name="db_writer",
    author="Imri Shai",
    version="1.0",
    packages=find_packages(),
    install_requires=["pika", "neo4j"],
)
