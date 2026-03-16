from setuptools import setup, find_packages

setup(
    name="bacon_server",
    author="Imri Shai",
    version="1.0",
    packages=find_packages(),
    install_requires=["flask", "flask_cors", "neo4j"],
)
