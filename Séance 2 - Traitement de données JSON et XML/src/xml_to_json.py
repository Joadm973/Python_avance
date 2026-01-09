"""
Exercice 1 : Conversion XML → JSON
Charger un fichier XML de type books.xml, extraire les titres et auteurs,
et sauvegarder le tout dans un fichier books.json.
"""

import xml.etree.ElementTree as ET
import json
from pathlib import Path


def load_books_from_xml(xml_path: Path) -> list[dict]:
    """
    Charge un fichier XML de livres et extrait les informations.
    
    Args:
        xml_path: Chemin vers le fichier XML
        
    Returns:
        Liste de dictionnaires contenant les informations des livres
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    books = []
    for book in root.findall("book"):
        book_data = {
            "id": int(book.get("id", 0)),
            "title": book.find("title").text if book.find("title") is not None else "",
            "author": book.find("author").text if book.find("author") is not None else "",
            "year": int(book.find("year").text) if book.find("year") is not None else None,
            "genre": book.find("genre").text if book.find("genre") is not None else ""
        }
        books.append(book_data)
    
    return books


def save_to_json(data: list[dict], json_path: Path) -> None:
    """
    Sauvegarde les données dans un fichier JSON.
    
    Args:
        data: Données à sauvegarder
        json_path: Chemin vers le fichier JSON de sortie
    """
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"✅ Données sauvegardées dans {json_path}")


def main():
    # Chemins des fichiers
    base_path = Path(__file__).parent.parent
    xml_path = base_path / "data" / "books.xml"
    json_path = base_path / "output" / "books.json"
    
    # Créer le dossier output s'il n'existe pas
    json_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Charger les livres depuis le XML
    print(f"📖 Chargement du fichier XML: {xml_path}")
    books = load_books_from_xml(xml_path)
    
    # Afficher les livres
    print(f"\n📚 {len(books)} livres trouvés:")
    for book in books:
        print(f"  - {book['title']} par {book['author']} ({book['year']})")
    
    # Sauvegarder en JSON
    print(f"\n💾 Sauvegarde en JSON...")
    save_to_json(books, json_path)


if __name__ == "__main__":
    main()
