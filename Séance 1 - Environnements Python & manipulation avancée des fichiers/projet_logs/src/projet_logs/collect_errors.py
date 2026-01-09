from pathlib import Path
import shutil
from datetime import datetime

def traiter_logs(log_dir, output_file, archive_dir=None):
    raw_path = Path(log_dir)
    out_path = Path(output_file)
    
    # Création du dossier de sortie
    out_path.parent.mkdir(exist_ok=True, parents=True)

    # Ouverture du fichier de sortie en écriture
    with out_path.open("w", encoding="utf-8") as out:
        # Parcours des fichiers .log [cite: 52]
        for log_file in raw_path.glob("*.log"):
            try:
                content = log_file.read_text(encoding="utf-8")
                for line in content.splitlines():
                    # Filtrage des erreurs [cite: 52]
                    if "ERROR" in line:
                        out.write(f"[{log_file.name}] {line}\n")
                
                # Bonus : Archivage [cite: 66]
                if archive_dir:
                    archive_path = Path(archive_dir)
                    archive_path.mkdir(exist_ok=True)
                    shutil.move(str(log_file), str(archive_path / log_file.name))
                    
            except Exception as e:
                print(f"Erreur lors de la lecture de {log_file}: {e}")

if __name__ == "__main__":
    # Bonus : Dater le fichier de sortie [cite: 66]
    date_str = datetime.now().strftime("%Y%m%d")
    traiter_logs("raw_logs", f"output/errors_{date_str}.log", "archive")