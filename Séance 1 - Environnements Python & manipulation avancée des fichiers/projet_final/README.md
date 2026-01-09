# Projet Final - Traitement CSV & Logs

Mini-projet Python avancé démontrant la gestion des environnements avec **uv** et la manipulation avancée de fichiers.

## 📋 Description

Ce projet automatise le traitement et l'organisation de données :
- **Traitement CSV** : nettoyage, suppression des doublons et des valeurs nulles
- **Réorganisation de logs** : classement par niveau (INFO, DEBUG, WARNING, ERROR)
- **Génération de rapports** : statistiques et fichiers organisés en sortie

## 🏗️ Structure du Projet

```
projet_final/
├─ pyproject.toml          # Configuration du projet (dépendances)
├─ uv.lock                 # Verrouillage des dépendances
├─ .venv/                  # Environnement virtuel (créé par uv)
├─ README.md               # Ce fichier
│
├─ data/
│  └─ data.csv             # Données d'exemple
│
├─ raw_logs/
│  ├─ app_2025-09-01.log   # Logs bruts
│  └─ app_2025-09-02.log
│
├─ output/                 # Résultats générés (créé au runtime)
│  ├─ data_cleaned.csv     # CSV nettoyé
│  ├─ data_stats.txt       # Statistiques
│  └─ logs_organized/      # Logs réorganisés
│     ├─ info.log
│     ├─ warning.log
│     ├─ error.log
│     └─ debug.log
│
└─ src/
   ├─ main.py             # Point d'entrée principal
   ├─ __init__.py
   └─ utils/
      ├─ paths.py         # Gestion des chemins (pathlib)
      ├─ io.py            # Lecture/écriture de fichiers
      └─ __init__.py
```

## 🛠️ Installation & Configuration

### Prérequis

- **Python** ≥ 3.10
- **uv** (gestionnaire de paquets Python moderne)

### Étapes d'installation

1. **Cloner/accéder au dossier** :
   ```bash
   cd projet_final
   ```

2. **Synchroniser l'environnement** (crée `.venv/` et installe les dépendances) :
   ```bash
   uv sync
   ```

3. **(Optionnel) Vérifier les dépendances** :
   ```bash
   uv pip list
   ```

## 🚀 Utilisation

### Commande standard

```bash
uv run python src/main.py --input data/data.csv --logs raw_logs --out output
```

### Paramètres

- `--input, -i` (obligatoire) : Chemin du fichier CSV à traiter
- `--logs, -l` (obligatoire) : Répertoire contenant les fichiers `.log`
- `--out, -o` (obligatoire) : Répertoire de sortie pour les résultats

### Exemple avec chemins personnalisés

```bash
uv run python src/main.py -i data/data.csv -l raw_logs -o results
```

## 📊 Fonctionnalités

### Traitement CSV
- ✅ Lecture de fichiers CSV avec **pandas**
- ✅ Suppression des lignes vides et doublons
- ✅ Export d'un fichier nettoyé
- ✅ Génération de statistiques descriptives

### Réorganisation des logs
- ✅ Parsing des lignes au format `[TIMESTAMP] LEVEL: MESSAGE`
- ✅ Classement par niveau (INFO, DEBUG, WARNING, ERROR, OTHER)
- ✅ Export dans des fichiers séparés
- ✅ Gestion robuste des erreurs de parsing

### Gestion des fichiers
- ✅ Utilisation de **pathlib** pour les chemins cross-platform
- ✅ Création automatique des répertoires manquants
- ✅ Validation des entrées avec messages d'erreur clairs
- ✅ Support UTF-8 pour tous les fichiers texte

## 📦 Dépendances

```toml
pandas>=2.0.0   # Traitement de données tabulaires
pydantic>=2.0.0 # Validation de données (optionnel, extensible)
```

Les dépendances de développement (optionnelles) :
```toml
pytest>=7.0.0   # Tests unitaires
black>=23.0.0   # Formatage de code
ruff>=0.1.0     # Linting
```

## 🧪 Tests (Optionnel)

Pour installer les dépendances de développement :

```bash
uv sync --all-extras
```

Exécuter les tests :

```bash
uv run pytest tests/
```

## 🔍 Mise en évidence des bonnes pratiques

### 1️⃣ **Gestion d'environnement robuste**
- Configuration via `pyproject.toml` (moderne)
- Fichier `uv.lock` pour reproductibilité
- `.venv/` isolé, recréable avec `uv sync`

### 2️⃣ **Utilisation de pathlib**
- Chemins cross-platform (Windows, Linux, macOS)
- Pas de concaténation de strings
- API objet-orientée et lisible

### 3️⃣ **Gestion d'erreurs appropriée**
- Try/except spécifiques
- Messages d'erreur explicites
- Codes de sortie significatifs (0 = succès, 1+ = erreur)

### 4️⃣ **Code typé et documenté**
- Type hints (PEP 484)
- Docstrings détaillées (Args, Returns, Raises)
- Structure logique avec séparation des responsabilités

### 5️⃣ **Modules bien organisés**
- `utils/paths.py` : gestion des chemins
- `utils/io.py` : lecture/écriture
- `main.py` : orchestration et CLI

### 6️⃣ **Interface CLI conviviale**
- `argparse` pour arguments structurés
- Help automatique (`--help`)
- Messages utilisateur clairs avec emojis

## 📝 Exemple d'exécution

```
============================================================
🚀 Démarrage du traitement
============================================================
📊 Traitement du CSV...
   Lecture : data.csv
   Données initiales : 6 lignes, 5 colonnes
🧹 Nettoyage des données...
  → Suppression des lignes vides...
  → Suppression des doublons...
  → Réinitialisation de l'index...
   Après nettoyage : 6 lignes
💾 Export des données...
   → Exporté vers : data_cleaned.csv
   → Statistiques : data_stats.txt

📋 Traitement de 2 fichier(s) journal...
   Lecture : app_2025-09-01.log
   Lecture : app_2025-09-02.log
✍️  Écriture des logs organisés...
   → info.log : 7 entrée(s)
   → debug.log : 3 entrée(s)
   → warning.log : 2 entrée(s)
   → error.log : 1 entrée(s)

============================================================
✅ Traitement terminé avec succès !
📁 Résultats dans : output
============================================================
```

## 🔧 Maintenance

### Ajouter une nouvelle dépendance

```bash
uv add nom-du-package
```

Cela mettra à jour `pyproject.toml` et `uv.lock` automatiquement.

### Formater le code

```bash
uv run black src/
uv run ruff check src/ --fix
```

### Regénérer l'environnement

```bash
rm -r .venv
uv sync
```

## 📚 Ressources

- [Documentation uv](https://docs.astral.sh/uv/)
- [Documentation pandas](https://pandas.pydata.org/)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)
- [pathlib Documentation](https://docs.python.org/3/library/pathlib.html)

## 📄 Licence

Projet pédagogique - Ynov B3 Python Avancé

---

**Auteur** : Mini-projet TP  
**Date** : Décembre 2025  
**Environnement** : Python 3.10+
