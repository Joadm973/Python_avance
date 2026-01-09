# Séance 3 - Organisation du code & bonnes pratiques

## Objectifs
- Structurer un projet Python (modules, packages)
- Respecter les conventions PEP8
- Documenter avec `docstring` et `typing`
- Ajouter des logs pour tracer l'exécution

## Structure du projet

```
exercice/
├── pyproject.toml
├── README.md
├── script_monolithique.py    # Script original à refactoriser
└── myapp/                    # Package refactorisé
    ├── __init__.py
    ├── main.py
    └── api.py
```

## Exercices pratiques

### 1. Refactorisation
- Prendre le script unique `script_monolithique.py`
- Le transformer en package avec plusieurs modules

### 2. Documentation
- Ajouter des `docstrings` et du `typing` à toutes les fonctions

### 3. Logs
- Remplacer tous les `print()` par `logging`
- Tester différents niveaux de log

### 4. Style
- Vérifier le code avec `flake8`
- Reformater avec `black`

## Installation

```bash
# Créer l'environnement virtuel
uv venv .venv

# Activer l'environnement (Windows)
.venv\Scripts\Activate.ps1

# Installer les dépendances
uv pip install -e .

# Installer les outils de développement
uv pip install black flake8
```

## Utilisation

```bash
# Lancer le script monolithique (avant refactorisation)
python script_monolithique.py

# Lancer le package refactorisé (après refactorisation)
python -m myapp.main
```

## Vérification du style

```bash
# Vérifier avec flake8
flake8 myapp/

# Formater avec black
black myapp/
```
