"""
Traitement de CSV et réorganisation de fichiers journaux.
Point d'entrée principal du projet.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional
import re
import pandas as pd

from utils.io import (
    read_csv,
    write_csv,
    read_log_file,
    write_text_file,
    get_all_log_files,
)
from utils.paths import (
    validate_input_path,
    get_output_dir,
)


def parse_log_entry(log_line: str) -> dict[str, str] | None:
    """
    Parse une ligne de journal au format [TIMESTAMP] LEVEL: MESSAGE.
    
    Args:
        log_line: Ligne du journal
    
    Returns:
        Dictionnaire avec 'timestamp', 'level', 'message' ou None si format invalide
    """
    # Pattern: [YYYY-MM-DD HH:MM:SS] LEVEL: MESSAGE
    pattern = r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\]\s+(\w+):\s+(.*)'
    match = re.match(pattern, log_line)
    
    if match:
        return {
            'timestamp': match.group(1),
            'level': match.group(2),
            'message': match.group(3),
        }
    return None


def clean_csv_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie les données CSV : suppression des doublons, valeurs nulles, etc.
    
    Args:
        df: DataFrame à nettoyer
    
    Returns:
        DataFrame nettoyé
    """
    print("  → Suppression des lignes vides...")
    df = df.dropna(how='all')
    
    print("  → Suppression des doublons...")
    df = df.drop_duplicates()
    
    print("  → Réinitialisation de l'index...")
    df = df.reset_index(drop=True)
    
    return df


def organize_logs(logs_dir: Path | str, output_dir: Path) -> None:
    """
    Réorganise les fichiers journaux par niveau (INFO, WARNING, ERROR, DEBUG).
    
    Args:
        logs_dir: Répertoire contenant les logs
        output_dir: Répertoire de sortie
    """
    logs_path = Path(logs_dir)
    validate_input_path(logs_path, must_exist=True)
    
    # Récupérer tous les fichiers .log
    log_files = get_all_log_files(logs_path)
    
    if not log_files:
        print(f"⚠️  Aucun fichier .log trouvé dans {logs_path}")
        return
    
    # Dictionnaire pour stocker les logs par niveau
    logs_by_level: dict[str, list[str]] = {
        'INFO': [],
        'DEBUG': [],
        'WARNING': [],
        'ERROR': [],
        'OTHER': [],
    }
    
    print(f"📋 Traitement de {len(log_files)} fichier(s) journal...")
    
    # Traiter chaque fichier
    for log_file in log_files:
        print(f"   Lecture : {log_file.name}")
        lines = read_log_file(log_file)
        
        for line in lines:
            parsed = parse_log_entry(line)
            if parsed:
                level = parsed['level']
                if level in logs_by_level:
                    logs_by_level[level].append(line)
                else:
                    logs_by_level['OTHER'].append(line)
            else:
                logs_by_level['OTHER'].append(line)
    
    # Écrire les logs organisés
    print("✍️  Écriture des logs organisés...")
    logs_output_dir = output_dir / "logs_organized"
    logs_output_dir.mkdir(parents=True, exist_ok=True)
    
    for level, entries in logs_by_level.items():
        if entries:
            output_file = logs_output_dir / f"{level.lower()}.log"
            content = '\n'.join(entries) + '\n'
            write_text_file(content, output_file, append=False)
            print(f"   → {level}.log : {len(entries)} entrée(s)")


def process_csv(csv_path: Path | str, output_dir: Path) -> None:
    """
    Traite le fichier CSV : nettoyage et export.
    
    Args:
        csv_path: Chemin du fichier CSV
        output_dir: Répertoire de sortie
    """
    csv_file = validate_input_path(csv_path, must_exist=True)
    
    print("📊 Traitement du CSV...")
    
    # Lire le CSV
    print(f"   Lecture : {csv_file.name}")
    df = read_csv(csv_file)
    print(f"   Données initiales : {len(df)} lignes, {len(df.columns)} colonnes")
    
    # Nettoyer
    print("🧹 Nettoyage des données...")
    df_clean = clean_csv_data(df)
    print(f"   Après nettoyage : {len(df_clean)} lignes")
    
    # Exporter
    print("💾 Export des données...")
    output_file = output_dir / "data_cleaned.csv"
    write_csv(df_clean, output_file, index=False)
    print(f"   → Exporté vers : {output_file.name}")
    
    # Générer des statistiques
    stats_file = output_dir / "data_stats.txt"
    stats_content = f"""=== Statistiques du traitement ===

Fichier source: {csv_file.name}
Nombre de lignes (brut): {len(df)}
Nombre de lignes (nettoyé): {len(df_clean)}
Nombre de colonnes: {len(df_clean.columns)}
Colonnes: {', '.join(df_clean.columns)}

Résumé numérique:
{df_clean.describe().to_string()}
"""
    write_text_file(stats_content, stats_file)
    print(f"   → Statistiques : {stats_file.name}")


def main(
    input_csv: str,
    logs_dir: str,
    output_dir: str,
) -> int:
    """
    Fonction principale.
    
    Args:
        input_csv: Chemin du fichier CSV d'entrée
        logs_dir: Répertoire des logs
        output_dir: Répertoire de sortie
    
    Returns:
        Code de sortie (0 = succès)
    """
    try:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        print("=" * 60)
        print("🚀 Démarrage du traitement")
        print("=" * 60)
        
        # Traiter le CSV
        process_csv(input_csv, output_path)
        
        print()
        
        # Réorganiser les logs
        organize_logs(logs_dir, output_path)
        
        print()
        print("=" * 60)
        print("✅ Traitement terminé avec succès !")
        print(f"📁 Résultats dans : {output_path}")
        print("=" * 60)
        
        return 0
    
    except FileNotFoundError as e:
        print(f"❌ Erreur : {e}", file=sys.stderr)
        return 1
    
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}", file=sys.stderr)
        return 2


def parse_arguments() -> argparse.Namespace:
    """Parse les arguments de ligne de commande."""
    parser = argparse.ArgumentParser(
        description="Traitement de CSV et réorganisation de fichiers journaux.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python src/main.py --input data/data.csv --logs raw_logs --out output
  python src/main.py -i data.csv -l logs -o results
        """,
    )
    
    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help="Chemin du fichier CSV d'entrée",
    )
    
    parser.add_argument(
        '--logs', '-l',
        type=str,
        required=True,
        help="Répertoire contenant les fichiers journaux",
    )
    
    parser.add_argument(
        '--out', '-o',
        type=str,
        required=True,
        help="Répertoire de sortie pour les résultats",
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    exit_code = main(
        input_csv=args.input,
        logs_dir=args.logs,
        output_dir=args.out,
    )
    sys.exit(exit_code)
