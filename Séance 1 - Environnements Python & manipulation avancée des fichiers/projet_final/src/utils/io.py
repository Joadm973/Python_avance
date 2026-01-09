"""
Utilitaires pour la lecture et l'écriture de fichiers.
"""

import csv
from pathlib import Path
from typing import Any, Optional
import pandas as pd


def read_csv(filepath: Path | str) -> pd.DataFrame:
    """
    Lit un fichier CSV et retourne un DataFrame pandas.
    
    Args:
        filepath: Chemin du fichier CSV
    
    Returns:
        DataFrame contenant les données CSV
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        pd.errors.ParserError: Si le CSV est mal formaté
    """
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"Fichier CSV non trouvé : {path}")
    
    try:
        df = pd.read_csv(path)
        return df
    except pd.errors.ParserError as e:
        raise pd.errors.ParserError(f"Erreur lors de la lecture du CSV : {e}")


def write_csv(df: pd.DataFrame, filepath: Path | str, index: bool = False) -> None:
    """
    Écrit un DataFrame pandas dans un fichier CSV.
    
    Args:
        df: DataFrame à écrire
        filepath: Chemin de destination
        index: Si True, inclut l'index dans le fichier
    
    Raises:
        IOError: En cas d'erreur d'écriture
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        df.to_csv(path, index=index)
    except IOError as e:
        raise IOError(f"Erreur lors de l'écriture du CSV : {e}")


def read_log_file(filepath: Path | str) -> list[str]:
    """
    Lit un fichier journal ligne par ligne.
    
    Args:
        filepath: Chemin du fichier journal
    
    Returns:
        Liste de lignes (sans caractères newline)
    
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
    """
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"Fichier journal non trouvé : {path}")
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = [line.rstrip('\n') for line in f]
        return lines
    except Exception as e:
        raise IOError(f"Erreur lors de la lecture du fichier journal : {e}")


def write_text_file(content: str, filepath: Path | str, append: bool = False) -> None:
    """
    Écrit du contenu texte dans un fichier.
    
    Args:
        content: Contenu à écrire
        filepath: Chemin de destination
        append: Si True, ajoute à la fin du fichier; sinon, remplace
    
    Raises:
        IOError: En cas d'erreur d'écriture
    """
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        mode = 'a' if append else 'w'
        with open(path, mode, encoding='utf-8') as f:
            f.write(content)
    except IOError as e:
        raise IOError(f"Erreur lors de l'écriture du fichier : {e}")


def get_all_log_files(logs_dir: Path | str) -> list[Path]:
    """
    Récupère tous les fichiers .log d'un répertoire.
    
    Args:
        logs_dir: Répertoire contenant les logs
    
    Returns:
        Liste de chemins des fichiers .log triés
    
    Raises:
        NotADirectoryError: Si le chemin n'est pas un répertoire
    """
    logs_path = Path(logs_dir)
    
    if not logs_path.is_dir():
        raise NotADirectoryError(f"Le chemin n'est pas un répertoire : {logs_path}")
    
    log_files = sorted(logs_path.glob("*.log"))
    return log_files
