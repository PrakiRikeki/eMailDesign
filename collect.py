import os

def generate_file_summary(start_path, output_filename="projekt_uebersicht.txt",
                        exclude_dirs=None, exclude_extensions=None):
    """
    Generiert eine Textdatei, die die Dateistruktur und den Inhalt aller Dateien
    in einem Startverzeichnis enthält.

    Args:
        start_path (str): Das Startverzeichnis, das durchsucht werden soll.
        output_filename (str): Der Name der Ausgabedatei.
        exclude_dirs (list, optional): Eine Liste von Ordnernamen, die ignoriert werden sollen.
                                        Standardmäßig ['__pycache__', '.git', 'node_modules', '.vscode'].
        exclude_extensions (list, optional): Eine Liste von Dateierweiterungen,
                                            die ignoriert werden sollen (z.B. ['.pyc', '.log']).
                                            Standardmäßig ['.pyc', '.log', '.jpg', '.png', '.gif', '.zip', '.rar', '.pdf'].
    """
    if exclude_dirs is None:
        exclude_dirs = ['__pycache__', '.git', 'node_modules', '.vscode']
    if exclude_extensions is None:
        exclude_extensions = ['.pyc', '.log', '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico',
                            '.zip', '.rar', '.7z', '.tar', '.gz', '.svg', '.json', '.lock', '.md',
                            '.pdf', '.exe', '.dll', '.bin', '.obj', '.so', '.woff', '.woff2', '.ttf', '.eot',
                            '.sqlite3', '.db', '.DS_Store']

    output_content = []
    output_content.append("=" * 80)
    output_content.append(f" PROJEKTÜBERSICHT: {os.path.basename(start_path)}")
    output_content.append("=" * 80)
    output_content.append("\n")

    # --- Teil 1: Dateistruktur (Baumansicht) ---
    output_content.append("### DATEISTRUKTUR ###\n")
    output_content.append("-" * 20 + "\n")

    for root, dirs, files in os.walk(start_path, topdown=True):
        # Exclude directories *before* walking into them
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        level = root.replace(start_path, '').count(os.sep)
        indent = '    ' * level
        base_name = os.path.basename(root)

        if root == start_path:  # Root directory
            output_content.append(f"{base_name}/\n")
        else:
            output_content.append(f"{indent}├── {base_name}/\n")

        subindent = '    ' * (level + 1)
        for f in files:
            if not any(f.endswith(ext) for ext in exclude_extensions):
                output_content.append(f"{subindent}├── {f}\n")
        
        # Optional: Indicate empty directories if desired
        if not files and not dirs and root != start_path:
            if os.path.exists(root) and not os.listdir(root): # Check if directory is actually empty
                pass # Currently, we don't explicitly mark empty leaf dirs, as os.walk handles them implicitly
                    # If you want to, add: output_content.append(f"{subindent}└── (leerer Ordner)\n")

    output_content.append("\n" * 2)

    # --- Teil 2: Dateiinhalt ---
    output_content.append("### DATEIINHALTE ###\n")
    output_content.append("-" * 20 + "\n")

    for root, dirs, files in os.walk(start_path, topdown=True):
        # Exclude directories again for content processing
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        for filename in files:
            file_path = os.path.join(root, filename)
            # Check if extension is excluded
            if any(filename.endswith(ext) for ext in exclude_extensions):
                continue

            # Check if directory containing file is excluded (should already be handled by dirs[:])
            if any(exclude_dir in file_path.split(os.sep) for exclude_dir in exclude_dirs):
                continue

            relative_path = os.path.relpath(file_path, start_path)
            output_content.append("\n" * 3)
            output_content.append("=" * 70)
            output_content.append(f" Datei: {relative_path} ")
            output_content.append("=" * 70)
            output_content.append("\n")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    output_content.append(content)
            except UnicodeDecodeError:
                output_content.append(f"ACHTUNG: Datei '{relative_path}' konnte nicht als UTF-8 dekodiert werden. Inhalt wird übersprungen (evtl. Binärdatei).")
            except Exception as e:
                output_content.append(f"Fehler beim Lesen der Datei '{relative_path}': {e}")

    # Write everything to the output file
    try:
        with open(output_filename, 'w', encoding='utf-8') as outfile:
            outfile.write("\n".join(output_content))
        print(f"Erfolgreich 'projekt_uebersicht.txt' erstellt im Verzeichnis: {os.getcwd()}")
    except Exception as e:
        print(f"Fehler beim Schreiben der Ausgabedatei: {e}")

if __name__ == "__main__":
    # --- KONFIGURATION ---
    # !!! WICHTIG: Pfad zu Ihrem Projektordner anpassen !!!
    START_PATH = "./"  # Beispiel: "C:\\Users\\IhrName\\Documents\\MeinProjekt" oder "./" für das aktuelle Verzeichnis

    # Liste von Ordnern, die NICHT in die Ausgabe aufgenommen werden sollen
    EXCLUDE_DIRECTORIES = ['__pycache__', '.git', 'node_modules', '.vscode', 'venv', 'env', '.idea', 'target', 'build', 'dist']

    # Liste von Dateierweiterungen, die NICHT in die Ausgabe aufgenommen werden sollen
    EXCLUDE_EXTENSIONS = [
        '.pyc', '.log', '.tmp', '.DS_Store',
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg', # Bilder
        '.zip', '.rar', '.7z', '.tar', '.gz', '.pdf', '.docx', '.xlsx', '.pptx', # Archive/Dokumente
        '.exe', '.dll', '.bin', '.obj', '.so', '.class', # Kompilierte/Binärdateien
        '.woff', '.woff2', '.ttf', '.eot', # Schriftarten
        '.sqlite3', '.db', # Datenbankdateien
        '.env', '.json', '.lock', '.toml', '.yaml', '.yml', '.md', # Konfigurations-/Meta-Dateien, wenn nicht explizit benötigt
        '.bak', '.old', # Backup-Dateien
    ]
    # --- ENDE KONFIGURATION ---

    # Überprüfen, ob der Startpfad existiert
    if not os.path.isdir(START_PATH):
        print(f"Fehler: Der angegebene Pfad '{START_PATH}' existiert nicht oder ist kein Verzeichnis.")
    else:
        generate_file_summary(START_PATH,
                            exclude_dirs=EXCLUDE_DIRECTORIES,
                            exclude_extensions=EXCLUDE_EXTENSIONS)