"""
Module principal - Point d'entrée de l'application.

Ce module configure le logging et orchestre l'exécution du programme.
"""

import logging
from .api import fetch_post

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main() -> None:
    """
    Point d'entrée principal de l'application.

    Récupère un post depuis l'API et affiche son contenu.

    Returns:
        None
    """
    logger.info("Démarrage du programme")

    try:
        post = fetch_post(1)
        logger.info("Post récupéré avec succès")
        print(post)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du post: {e}")
        raise


if __name__ == "__main__":
    main()
