"""
Exercice 2 : Fusion JSON
Charger plusieurs fichiers JSON (data1.json, data2.json),
les fusionner en un seul dataset, éliminer les doublons,
et sauvegarder dans merged.json.
"""

import json
from pathlib import Path


def load_json(json_path: Path) -> list[dict]:
    """
    Charge un fichier JSON et retourne son contenu.
    
    Args:
        json_path: Chemin vers le fichier JSON
        
    Returns:
        Liste de dictionnaires
    """
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"📄 Chargé {len(data)} entrées depuis {json_path.name}")
    return data


def merge_datasets(datasets: list[list[dict]], key: str = "id") -> list[dict]:
    """
    Fusionne plusieurs datasets et élimine les doublons basés sur une clé.
    
    Args:
        datasets: Liste de datasets à fusionner
        key: Clé utilisée pour identifier les doublons
        
    Returns:
        Dataset fusionné sans doublons
    """
    seen_keys = set()
    merged = []
    
    for dataset in datasets:
        for item in dataset:
            item_key = item.get(key)
            if item_key not in seen_keys:
                seen_keys.add(item_key)
                merged.append(item)
    
    return merged


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
    data_path = base_path / "data"
    output_path = base_path / "output" / "merged.json"
    
    # Créer le dossier output s'il n'existe pas
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Charger les fichiers JSON
    print("📂 Chargement des fichiers JSON...")
    data1 = load_json(data_path / "data1.json")
    data2 = load_json(data_path / "data2.json")
    
    # Compter le total avant fusion
    total_before = len(data1) + len(data2)
    print(f"\n📊 Total avant fusion: {total_before} entrées")
    
    # Fusionner les datasets
    print("\n🔄 Fusion des datasets et élimination des doublons...")
    merged = merge_datasets([data1, data2], key="id")
    
    # Afficher les résultats
    duplicates_removed = total_before - len(merged)
    print(f"🗑️  {duplicates_removed} doublon(s) supprimé(s)")
    print(f"📊 Total après fusion: {len(merged)} entrées")
    
    # Afficher les données fusionnées
    print("\n👥 Données fusionnées:")
    for item in merged:
        print(f"  - {item['name']} ({item['email']}) - {item['city']}")
    
    # Sauvegarder le résultat
    print(f"\n💾 Sauvegarde...")
    save_to_json(merged, output_path)


if __name__ == "__main__":
    main()
