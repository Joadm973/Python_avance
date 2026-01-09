"""
Évaluation - Mini-projet : Script de parsing multi-format
==========================================================

Objectifs :
- Lecture d'un fichier data.json ou data.xml
- Détection automatique du format
- Transformation vers un format standard Python (dict ou list)
- Gestion des erreurs (fichier vide, mauvais format, clé manquante)
"""

import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any
from enum import Enum


class FileFormat(Enum):
    """Enumération des formats de fichiers supportés."""
    JSON = "json"
    XML = "xml"
    UNKNOWN = "unknown"


class ParserError(Exception):
    """Exception personnalisée pour les erreurs de parsing."""
    pass


class EmptyFileError(ParserError):
    """Exception levée quand le fichier est vide."""
    pass


class InvalidFormatError(ParserError):
    """Exception levée quand le format est invalide."""
    pass


class MissingKeyError(ParserError):
    """Exception levée quand une clé est manquante."""
    pass


def detect_format(file_path: Path) -> FileFormat:
    """
    Détecte automatiquement le format d'un fichier basé sur son extension
    et son contenu.
    
    Args:
        file_path: Chemin vers le fichier
        
    Returns:
        FileFormat correspondant au type détecté
    """
    extension = file_path.suffix.lower()
    
    if extension == ".json":
        return FileFormat.JSON
    elif extension == ".xml":
        return FileFormat.XML
    else:
        # Tenter de détecter par le contenu
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return FileFormat.UNKNOWN
                if content.startswith("{") or content.startswith("["):
                    return FileFormat.JSON
                elif content.startswith("<?xml") or content.startswith("<"):
                    return FileFormat.XML
        except Exception:
            pass
        
        return FileFormat.UNKNOWN


def parse_json(file_path: Path) -> dict | list:
    """
    Parse un fichier JSON et retourne son contenu.
    
    Args:
        file_path: Chemin vers le fichier JSON
        
    Returns:
        Contenu du fichier sous forme de dict ou list
        
    Raises:
        EmptyFileError: Si le fichier est vide
        InvalidFormatError: Si le JSON est invalide
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    if not content:
        raise EmptyFileError(f"Le fichier '{file_path.name}' est vide")
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        raise InvalidFormatError(f"Format JSON invalide dans '{file_path.name}': {e}")


def parse_xml(file_path: Path) -> dict:
    """
    Parse un fichier XML et retourne son contenu sous forme de dictionnaire.
    
    Args:
        file_path: Chemin vers le fichier XML
        
    Returns:
        Contenu du fichier sous forme de dict
        
    Raises:
        EmptyFileError: Si le fichier est vide
        InvalidFormatError: Si le XML est invalide
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    
    if not content:
        raise EmptyFileError(f"Le fichier '{file_path.name}' est vide")
    
    try:
        root = ET.fromstring(content)
        return xml_element_to_dict(root)
    except ET.ParseError as e:
        raise InvalidFormatError(f"Format XML invalide dans '{file_path.name}': {e}")


def xml_element_to_dict(element: ET.Element) -> dict:
    """
    Convertit récursivement un élément XML en dictionnaire Python.
    
    Args:
        element: Élément XML à convertir
        
    Returns:
        Dictionnaire représentant l'élément XML
    """
    result = {}
    
    # Ajouter les attributs
    if element.attrib:
        result["@attributes"] = dict(element.attrib)
    
    # Traiter les enfants
    children = list(element)
    if children:
        child_dict = {}
        for child in children:
            child_data = xml_element_to_dict(child)
            
            # Gérer les éléments multiples avec le même nom (liste)
            if child.tag in child_dict:
                if not isinstance(child_dict[child.tag], list):
                    child_dict[child.tag] = [child_dict[child.tag]]
                child_dict[child.tag].append(child_data)
            else:
                child_dict[child.tag] = child_data
        
        result.update(child_dict)
    elif element.text and element.text.strip():
        # Convertir les types de base
        text = element.text.strip()
        return convert_value(text)
    
    return result


def convert_value(value: str) -> Any:
    """
    Convertit une chaîne en son type Python approprié.
    
    Args:
        value: Valeur à convertir
        
    Returns:
        Valeur convertie (int, float, bool ou str)
    """
    # Boolean
    if value.lower() == "true":
        return True
    elif value.lower() == "false":
        return False
    
    # Integer
    try:
        return int(value)
    except ValueError:
        pass
    
    # Float
    try:
        return float(value)
    except ValueError:
        pass
    
    # String
    return value


def get_value(data: dict, key: str, required: bool = True) -> Any:
    """
    Récupère une valeur d'un dictionnaire avec gestion des clés manquantes.
    
    Args:
        data: Dictionnaire source
        key: Clé à récupérer
        required: Si True, lève une exception si la clé est manquante
        
    Returns:
        Valeur associée à la clé
        
    Raises:
        MissingKeyError: Si la clé est manquante et required=True
    """
    if key not in data:
        if required:
            raise MissingKeyError(f"Clé manquante: '{key}'")
        return None
    return data[key]


def parse_file(file_path: str | Path) -> dict | list:
    """
    Fonction principale : parse un fichier JSON ou XML automatiquement.
    
    Args:
        file_path: Chemin vers le fichier à parser
        
    Returns:
        Contenu du fichier sous forme de dict ou list
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        EmptyFileError: Si le fichier est vide
        InvalidFormatError: Si le format est invalide ou non supporté
    """
    path = Path(file_path)
    
    # Vérifier que le fichier existe
    if not path.exists():
        raise FileNotFoundError(f"Fichier non trouvé: '{path}'")
    
    # Détecter le format
    file_format = detect_format(path)
    print(f"📄 Fichier: {path.name}")
    print(f"🔍 Format détecté: {file_format.value.upper()}")
    
    # Parser selon le format
    if file_format == FileFormat.JSON:
        return parse_json(path)
    elif file_format == FileFormat.XML:
        return parse_xml(path)
    else:
        raise InvalidFormatError(
            f"Format non supporté pour '{path.name}'. "
            "Formats acceptés: JSON, XML"
        )


def display_data(data: dict | list, indent: int = 0) -> None:
    """
    Affiche les données de manière formatée.
    
    Args:
        data: Données à afficher
        indent: Niveau d'indentation
    """
    prefix = "  " * indent
    
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                print(f"{prefix}📁 {key}:")
                display_data(value, indent + 1)
            else:
                print(f"{prefix}• {key}: {value}")
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print(f"{prefix}[{i}]")
            display_data(item, indent + 1)
    else:
        print(f"{prefix}{data}")


def main():
    """Point d'entrée principal avec démonstration des fonctionnalités."""
    base_path = Path(__file__).parent
    data_path = base_path / "data"
    
    # Liste des fichiers à tester
    test_files = [
        ("data.json", "Fichier JSON valide"),
        ("data.xml", "Fichier XML valide"),
        ("empty.json", "Fichier vide"),
        ("invalid.txt", "Format non supporté"),
        ("nonexistent.json", "Fichier inexistant"),
    ]
    
    print("=" * 60)
    print("🔧 MINI-PROJET : Parser Multi-Format (JSON/XML)")
    print("=" * 60)
    
    for filename, description in test_files:
        print(f"\n{'─' * 60}")
        print(f"📋 Test: {description}")
        print(f"{'─' * 60}")
        
        file_path = data_path / filename
        
        try:
            data = parse_file(file_path)
            print(f"✅ Parsing réussi!")
            print(f"\n📊 Type de données: {type(data).__name__}")
            print(f"\n📝 Contenu:")
            display_data(data)
            
            # Démonstration de get_value avec gestion d'erreur
            if isinstance(data, dict):
                print(f"\n🔑 Test d'accès aux clés:")
                try:
                    products = get_value(data, "products")
                    print(f"  ✅ Clé 'products' trouvée ({len(products) if isinstance(products, list) else 'dict'})")
                except MissingKeyError as e:
                    print(f"  ⚠️ {e}")
                
                try:
                    missing = get_value(data, "nonexistent_key")
                except MissingKeyError as e:
                    print(f"  ⚠️ {e}")
                    
        except FileNotFoundError as e:
            print(f"❌ Erreur: {e}")
        except EmptyFileError as e:
            print(f"❌ Erreur: {e}")
        except InvalidFormatError as e:
            print(f"❌ Erreur: {e}")
        except ParserError as e:
            print(f"❌ Erreur de parsing: {e}")
    
    print(f"\n{'=' * 60}")
    print("✨ Tous les tests terminés!")
    print("=" * 60)


if __name__ == "__main__":
    main()
