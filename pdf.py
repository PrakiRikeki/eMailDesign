import os
from bs4 import BeautifulSoup

def combine_html_files(index_html_path, files_dir, output_html_path):
    """
    Kombiniert eine Haupt-HTML-Datei (als Inhaltsverzeichnis) und alle verlinkten HTML-Dateien
    in einem Unterordner zu einer einzigen großen HTML-Datei.

    Args:
        index_html_path (str): Pfad zur index.html-Datei, die als Inhaltsverzeichnis dient.
        files_dir (str): Pfad zum Ordner, der die verlinkten HTML-Dateien enthält.
        output_html_path (str): Pfad zur Ausgabe-HTML-Datei.
    """
    print(f"Starte die Kombination von '{index_html_path}' und '{files_dir}' zu einer HTML-Datei...")

    base_dir = os.path.dirname(index_html_path)
    combined_body_content = "" # Hier sammeln wir den Inhalt des Body-Tags

    # Grundlegendes CSS für die kombinierte HTML-Datei, um die Darstellung zu verbessern
    # und Seitenumbrüche für PDF-Export vorzubereiten.
    combined_css = """
    <style type="text/css">
        body {
            font-family: 'Inter', Arial, sans-serif;
            margin: 0;
            padding: 0;
            line-height: 1.6;
            background-color: #f8fafc;
        }
        /* Style für den Hauptcontainer, der die E-Mails umhüllt */
        .email-wrapper-outer {
            padding: 48px 24px; /* Äußeres Padding wie in den Original-E-Mails */
            width: 100%;
            display: block;
        }
        .email-container {
            width: 90%;
            max-width: 700px;
            margin: 0 auto;
            background-color: #ffffff;
            border-radius: 24px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
            overflow: hidden;
            margin-bottom: 2cm; /* Platz zwischen den E-Mails im kombinierten HTML */
            box-sizing: border-box; /* Padding/Border in der Breite mitberechnen */
        }

        /* Überschriften der einzelnen E-Mails im kombinierten Dokument */
        .email-section-title {
            text-align: center;
            background-color: #e0f2fe; /* Leichter Hintergrund für die E-Mail-Titel */
            padding: 32px;
            border-radius: 24px 24px 0 0;
            margin-bottom: 0; /* Überschrift direkt am Inhalt */
        }
        .email-section-title h1 {
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin: 0 0 8px 0;
        }
        .email-section-title p {
            margin: 0;
            font-size: 18px;
            color: #475569;
            padding-bottom: 0px;
        }

        /* Um sicherzustellen, dass jede E-Mail eine neue Seite im PDF beginnt */
        /* Dies funktioniert am besten beim Drucken aus Browsern */
        .page-break-before {
            page-break-before: always;
            break-before: page; /* Für modernere Browser */
        }
        
        /* Links im Inhaltsverzeichnis */
        .toc-list ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .toc-list li {
            margin-bottom: 8px;
        }
        .toc-list a {
            font-size: 16px;
            color: #00aeef;
            text-decoration: underline;
        }
        .toc-list a:hover {
            color: #008cd4;
        }
    </style>
    """

    # 1. index.html als Inhaltsverzeichnis verarbeiten
    try:
        with open(index_html_path, 'r', encoding='utf-8') as f:
            index_soup = BeautifulSoup(f.read(), 'html.parser')
            
            # Ändere die Links in der index.html, um auf Anker innerhalb des finalen HTML zu verweisen
            # Der Anker wird der Dateiname ohne Erweiterung sein
            for a_tag in index_soup.select('td ul li a'):
                original_href = a_tag['href']
                
                # Wir müssen den Pfad relativ zum 'dateien' Ordner extrahieren
                if original_href.startswith("dateien/"):
                    filename = os.path.basename(original_href)
                    anchor_name = os.path.splitext(filename)[0]
                    a_tag['href'] = f'#{anchor_name}'
                    print(f"Link '{original_href}' in TOC geändert zu '#{anchor_name}'")
                elif original_href == "index.html" or original_href.startswith("./index.html") or original_href == "index.html":
                    a_tag['href'] = '#top' # Link zum Anfang des Dokuments
                    print(f"Link '{original_href}' in TOC geändert zu '#top'")
                else:
                    # Externe Links oder andere interne Links bleiben unverändert
                    pass

            # Füge einen Anker an den Anfang der index.html für den "Index-Seite" Link
            # Wir umhüllen den Haupt-Inhaltsbereich der index.html mit einer speziellen Klasse und ID
            index_main_container = index_soup.find('table', width="90%", style=lambda s: s and 'max-width: 700px' in s)
            
            if index_main_container:
                # Füge den Anker und eine Überschrift für das Inhaltsverzeichnis hinzu
                index_main_container.insert(0, index_soup.new_tag('a', id='top'))
                
                # Wenn der Header der index.html bereits Titel und Untertitel hat, verwenden wir diese
                # Ansonsten fügen wir einen generischen Titel ein
                header_content = index_main_container.find('table', style=lambda s: s and 'background-color: #e0f2fe' in s)
                if header_content:
                    # Entferne das body tag, um doppelte zu vermeiden
                    for tag in index_main_container.find_all('body'):
                        tag.unwrap()
                    combined_body_content += f'<div class="email-wrapper-outer"><div class="email-container">{str(index_main_container)}</div></div>'
                else:
                    # Fallback für den Fall, dass die Struktur anders ist
                    combined_body_content += f'<div class="email-wrapper-outer"><div class="email-container"><a id="top"></a><div class="email-section-title"><h1>Inhaltsverzeichnis E-Mail-Vorlagen</h1><p>Alle Vorlagen im Überblick</p></div>{str(index_soup.body.contents)}</div></div>'
            else:
                 print(f"Warnung: Haupt-E-Mail-Container in '{index_html_path}' nicht gefunden. Verwende gesamten Body-Inhalt.")
                 if index_soup.body:
                     combined_body_content += f'<div class="email-wrapper-outer"><div class="email-container"><a id="top"></a><div class="email-section-title"><h1>Inhaltsverzeichnis E-Mail-Vorlagen</h1><p>Alle Vorlagen im Überblick</p></div>{str(index_soup.body.contents)}</div></div>'
                 else:
                     print(f"Fehler: Konnte keinen Body-Inhalt in '{index_html_path}' finden, überspringe.")


    except Exception as e:
        print(f"Fehler beim Parsen oder Modifizieren von index.html: {e}")
        return

    # 2. Iteriere durch die Dateien im 'dateien/' Ordner
    # Sortiere die Dateien alphabetisch, damit die Reihenfolge konsistent ist
    for filename in sorted(os.listdir(files_dir)):
        if filename.endswith(".html") and filename != "index.html": # index.html des Unterordners ignorieren
            file_path = os.path.join(files_dir, filename)
            email_id = os.path.splitext(filename)[0] # z.B. 'anfrage_hotel_hotelbetreiber'

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    email_html = f.read()
                    email_soup = BeautifulSoup(email_html, 'html.parser')

                    # Extrahiere den Titel der E-Mail für die Sektionsüberschrift
                    title_tag = email_soup.find('title')
                    email_title = title_tag.get_text() if title_tag else os.path.basename(filename)

                    # Finde den Haupt-E-Mail-Container (die äußere weiße Box)
                    main_email_container = email_soup.find('table', width="90%", style=lambda s: s and 'max-width: 700px' in s)

                    if not main_email_container:
                        print(f"Warnung: Haupt-E-Mail-Container in '{filename}' nicht gefunden. Verwende body-Inhalt.")
                        body_content_tag = email_soup.body
                        if body_content_tag:
                            email_section_html = f'''
                                <div class="email-wrapper-outer page-break-before">
                                    <div class="email-container">
                                        <a id="{email_id}"></a>
                                        <div class="email-section-title">
                                            <h1>{email_title}</h1>
                                            <p>{title_tag.find_next_sibling('p').get_text() if title_tag and title_tag.find_next_sibling('p') else ''}</p>
                                        </div>
                                        {str(body_content_tag)}
                                    </div>
                                </div>
                            '''
                            combined_body_content += email_section_html
                        else:
                            print(f"Konnte keinen Body-Inhalt in '{filename}' finden, überspringe.")
                    else:
                        # Füge den Anker und eine Überschrift HIER vor dem main_email_container hinzu
                        # (innerhalb eines neuen div, das auch page-break-before bekommt)
                        
                        # Extrahiere den Header der E-Mail für den Titel
                        header_table = main_email_container.find('table', style=lambda s: s and 'background-color: #e0f2fe' in s)
                        header_html = ""
                        if header_table:
                            # Wir nehmen den vorhandenen Header aus der E-Mail-Struktur
                            # und passen ihn an unsere kombinierte Struktur an.
                            # Entferne ggf. vorhandene <img> Tags und füge sie extern hinzu
                            img_tag = header_table.find('img')
                            img_src = img_tag['src'] if img_tag else ''
                            if img_tag:
                                img_tag.extract() # Entferne das Bild aus dem Header, damit es nicht dupliziert wird
                            
                            h1_title = header_table.find('h1')
                            p_subtitle = header_table.find('p')

                            header_html = f'''
                                <div class="email-section-title">
                                    <img src="{img_src}" alt="ribeka Logo" width="150" height="auto" style="display: block; border: 0; margin: 0 auto 16px auto; max-width: 100%; line-height: 100%; outline: none; text-decoration: none;">
                                    <h1>{h1_title.get_text() if h1_title else email_title}</h1>
                                    <p>{p_subtitle.get_text() if p_subtitle else ''}</p>
                                </div>
                            '''
                            # Den Rest des Inhalts des main_email_containers nehmen wir ohne seinen Header
                            # main_email_container_without_header = main_email_container.find('table', style=lambda s: s and 'border-collapse: collapse' in s and 'background-color' not in s)
                            # Wenn wir den gesamten main_email_container nehmen, müssen wir sicherstellen, dass er nicht seinen eigenen Header dupliziert
                            # Ein einfacherer Ansatz ist, den Anker und den Titel vor dem gesamten Container zu platzieren
                            
                            # Da die Original-E-Mails bereits den Header im weißen Container haben,
                            # ist der einfachste Weg, den Anker und den page-break-before davor zu setzen
                            # und den vorhandenen Inhalt so zu übernehmen wie er ist.
                            
                            # Entferne doppeltes body-Tag, das BeautifulSoup manchmal hinzufügt
                            for tag in main_email_container.find_all('body'):
                                tag.unwrap()

                            email_section_html = f'''
                                <div class="email-wrapper-outer page-break-before">
                                    <div class="email-container">
                                        <a id="{email_id}"></a>
                                        {str(main_email_container)}
                                    </div>
                                </div>
                            '''
                            combined_body_content += email_section_html

                    print(f"'{filename}' zum kombinierten HTML hinzugefügt.")

            except Exception as e:
                print(f"Fehler beim Lesen oder Parsen von '{file_path}': {e}")
    
    # Vollständiges HTML-Dokument erstellen
    full_html_doc = f"""
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Projektübersicht E-Mail-Vorlagen</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
        {combined_css}
    </head>
    <body>
        {combined_body_content}
    </body>
    </html>
    """

    # Speichere die kombinierte HTML-Datei
    try:
        with open(output_html_path, "w", encoding="utf-8") as f:
            f.write(full_html_doc)
        print(f"Erfolgreich kombinierte HTML-Datei erstellt: '{output_html_path}'")
        print("\nSie können diese HTML-Datei nun in Ihrem Browser öffnen (z.B. Chrome, Firefox) und die Druckfunktion (STRG+P oder CMD+P) verwenden, um sie als PDF zu speichern.")
        print("Stellen Sie sicher, dass 'Hintergrundgrafiken' aktiviert sind, um das vollständige Design zu erhalten, und 'Layout: Hochformat'/'Größe: A4' eingestellt ist.")

    except Exception as e:
        print(f"Fehler beim Schreiben der Ausgabedatei: {e}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    INDEX_HTML = os.path.join(script_dir, 'index.html')
    FILES_DIR = os.path.join(script_dir, 'dateien')
    OUTPUT_HTML = os.path.join(script_dir, 'projekt_uebersicht_komplett.html')

    if not os.path.isdir(FILES_DIR):
        print(f"Fehler: Der Ordner '{FILES_DIR}' wurde nicht gefunden.")
    elif not os.path.isfile(INDEX_HTML):
        print(f"Fehler: Die Datei '{INDEX_HTML}' wurde nicht gefunden.")
    else:
        combine_html_files(INDEX_HTML, FILES_DIR, OUTPUT_HTML)