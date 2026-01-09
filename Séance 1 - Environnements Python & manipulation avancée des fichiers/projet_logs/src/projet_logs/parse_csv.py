import pandas as pd
from pathlib import Path

def nettoyer_csv(input_path, output_path):
    # 1. Lecture du fichier (séparateur et encodage spécifiés dans le cours) [cite: 46]
    # On gère les types si nécessaire avec dtype=str pour éviter les erreurs de conversion
    df = pd.read_csv(input_path, sep=";", encoding="utf-8", dtype=str)

    # 2. Nettoyage des noms de colonnes [cite: 47]
    # Strip (espaces), lower (minuscule), replace (espace par underscore)
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    # 3. Gestion des valeurs manquantes (Ex: dropna si la ligne est vide) [cite: 47]
    df = df.replace({"": None})
    df = df.dropna(how="all")

    # 4. Sauvegarde dans output/clean_data.csv [cite: 61]
    output_path = Path(output_path)
    output_path.parent.mkdir(exist_ok=True, parents=True) # Crée le dossier output si absent
    df.to_csv(output_path, index=False)
    print(f"Fichier nettoyé sauvegardé sous : {output_path}")

if __name__ == "__main__":
    # Chemins basés sur la structure demandée
    nettoyer_csv("data/data.csv", "output/clean_data.csv")