from setuptools import setup, find_packages

setup(
    name="bacon_distance",
    author="Imri Shai",
    version="1.0",
    packages=find_packages(),
    install_requires=["pandas", "networkx", "flask", "flask_cors"],
)
