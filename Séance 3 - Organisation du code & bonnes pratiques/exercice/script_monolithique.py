"""
Script monolithique à refactoriser.

Objectif : Transformer ce script en package Python structuré
avec documentation, typing et logging.
"""

import requests


def main():
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.get(url)
    print(response.json())


if __name__ == "__main__":
    main()
