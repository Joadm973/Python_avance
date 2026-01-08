# Projet Logs - Analyse et Traitement de Fichiers Journaux

Projet Python pour le traitement et l'analyse de fichiers logs avec **uv**.

## 📋 Description

Ce projet automatise l'analyse de fichiers journaux :
- **Collecte d'erreurs** : extraction des erreurs depuis les logs bruts
- **Traitement CSV** : analyse et nettoyage de données
- **Archivage** : organisation et stockage des logs traités

## 🏗️ Structure du Projet

```
projet_logs/
├─ pyproject.toml          # Configuration du projet (dépendances)
├─ uv.lock                 # Verrouillage des dépendances
├─ .venv/                  # Environnement virtuel (créé par uv)
├─ README.md               # Ce fichier
│
├─ data/
│  └─ data.csv             # Données d'exemple
│
├─ raw_logs/
│  └─ errors_20251205.log  # Logs bruts d'erreurs
│
├─ archive/                # Logs archivés
│  ├─ api_2025-01-12.log
│  ├─ app_2025-01-10.log
│  ├─ auth_2025-01-13.log
│  ├─ payment_2025-01-14.log
│  └─ server_2025-01-11.log
│
├─ output/                 # Résultats générés
│  └─ clean_data.csv       # CSV nettoyé
│
└─ src/
   └─ projet_logs/
      ├─ __init__.py
      ├─ collect_errors.py # Collecte des erreurs depuis les logs
      └─ parse_csv.py      # Traitement des fichiers CSV
```

## 🛠️ Installation & Configuration

### Prérequis

- **Python** ≥ 3.12
- **uv** installé ([Installation uv](https://github.com/astral-sh/uv))

### Installation avec uv

1. **Cloner le projet** :
   ```bash
   git clone <url-du-repo>
   cd projet_logs
   ```

2. **Créer l'environnement virtuel et installer les dépendances** :
   ```bash
   uv venv
   uv pip install -e .
   ```

3. **Activer l'environnement virtuel** :
   - Windows :
     ```powershell
     .venv\Scripts\activate
     ```
   - Linux/macOS :
     ```bash
     source .venv/bin/activate
     ```

## 🚀 Utilisation

### Exécuter le projet

```bash
uv run python -m projet_logs
```

### Collecter les erreurs des logs

```bash
uv run python -m projet_logs.collect_errors
```

### Traiter les fichiers CSV

```bash
uv run python -m projet_logs.parse_csv
```

## 📦 Dépendances

- **pandas** : manipulation et analyse de données
- **Python** : ≥ 3.12

## 📝 Fonctionnalités

### collect_errors.py
Module pour extraire et analyser les erreurs depuis les fichiers de logs.

### parse_csv.py
Module pour le traitement et le nettoyage des fichiers CSV.

## 🧪 Tests

Les tests peuvent être ajoutés dans un dossier `tests/` avec pytest :

```bash
uv pip install pytest
uv run pytest
```

## 📄 License

Projet académique - Ynov B3 Python Avancé

## 👤 Auteur

Josue Adami - josue.adami@ynov.com
