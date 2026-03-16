from setuptools import setup, find_packages

setup(
    name="db_initializer",
    author="Imri Shai",
    version="1.0",
    packages=find_packages(),
    install_requires=["pandas", "neo4j"],
)
