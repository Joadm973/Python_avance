"""
Utilitaires de gestion des chemins (pathlib).
"""

from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """Retourne le répertoire racine du projet."""
    return Path(__file__).parent.parent.parent


def get_data_dir(create: bool = False) -> Path:
    """
    Retourne le chemin du répertoire data/.
    
    Args:
        create: Si True, crée le répertoire s'il n'existe pas.
    
    Returns:
        Path du répertoire data/
    """
    data_dir = get_project_root() / "data"
    if create:
        data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_logs_dir(create: bool = False) -> Path:
    """
    Retourne le chemin du répertoire raw_logs/.
    
    Args:
        create: Si True, crée le répertoire s'il n'existe pas.
    
    Returns:
        Path du répertoire raw_logs/
    """
    logs_dir = get_project_root() / "raw_logs"
    if create:
        logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir


def get_output_dir(create: bool = False) -> Path:
    """
    Retourne le chemin du répertoire output/.
    
    Args:
        create: Si True, crée le répertoire s'il n'existe pas.
    
    Returns:
        Path du répertoire output/
    """
    output_dir = get_project_root() / "output"
    if create:
        output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def validate_input_path(filepath: Path | str, must_exist: bool = True) -> Path:
    """
    Valide qu'un chemin existe et est accessible.
    
    Args:
        filepath: Chemin à valider
        must_exist: Si True, vérifie que le fichier existe
    
    Returns:
        Path normalisé
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas et must_exist=True
        ValueError: Si le chemin n'est pas valide
    """
    path = Path(filepath)
    
    if must_exist and not path.exists():
        raise FileNotFoundError(f"Fichier ou répertoire non trouvé : {path}")
    
    return path
