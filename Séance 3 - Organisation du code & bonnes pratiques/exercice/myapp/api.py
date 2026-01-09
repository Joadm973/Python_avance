"""
Module API - Gestion des appels à l'API JSONPlaceholder.

Ce module contient les fonctions pour interagir avec l'API externe.
"""

import logging
import requests
from typing import Dict

logger = logging.getLogger(__name__)


def fetch_post(post_id: int) -> Dict:
    """
    Récupère un post par son ID depuis l'API JSONPlaceholder.

    Args:
        post_id (int): L'identifiant unique du post à récupérer.

    Returns:
        Dict: Les données du post sous forme de dictionnaire.

    Raises:
        requests.HTTPError: Si la requête échoue.

    Example:
        >>> post = fetch_post(1)
        >>> print(post['title'])
    """
    url = f"https://jsonplaceholder.typicode.com/posts/{post_id}"
    logger.debug(f"Requête vers {url}")

    response = requests.get(url)
    response.raise_for_status()

    logger.debug(f"Réponse reçue: status={response.status_code}")
    return response.json()
