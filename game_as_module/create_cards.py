# Importiere notwendige Bibliotheken
# PIL (Pillow) für die Bildverarbeitung
from PIL import Image, ImageDraw, ImageFont, ImageColor
# os für Operationen mit dem Betriebssystem, z.B. Erstellen von Verzeichnissen
import os

# Funktion zum Erstellen des Ausgabeverzeichnisses für die Kartenbilder
def create_output_directory():
    """
    Erstellt ein Verzeichnis namens 'karten_bilder', falls es noch nicht existiert.

    Returns:
        str: Der Pfad des erstellten (oder bereits existierenden) Verzeichnisses.
    """
    # Definiere den Namen des Ausgabeverzeichnisses
    output_dir = "karten_bilder"
    # Überprüfe, ob das Verzeichnis bereits existiert
    if not os.path.exists(output_dir):
        # Wenn nicht, erstelle es
        os.makedirs(output_dir)
    # Gib den Pfad des Verzeichnisses zurück
    return output_dir

# Funktion zum Erstellen der Kartenbilder
def create_card_images():
    """
    Generiert Kartenbilder für verschiedene Elemente und Kartennamen und speichert diese im Ausgabeverzeichnis.
    """
    # Liste der Spielelemente
    elements = ["Feuer", "Wasser", "Erde", "Luft", "Blitz", "Eis", "Magie"]

    # Liste der Kartennamen/Werte
    card_names = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Bube", "Dame", "Koenig", "Ass"
    ]

    # Definiere die Größe der Karten (Breite und Höhe)
    card_width, card_height = 500, 700

    # Definiere die Schriftart für die Texte auf den Karten
    try:
        # Versuche, die Schriftart "arialbd.ttf" zu laden und eine dynamische Schriftgröße zu setzen
        base_font_size = int(card_height * 0.08)  # Basisschriftgröße, proportional zur Kartenhöhe
        font = ImageFont.truetype("arialbd.ttf", base_font_size)
        # Erstelle eine kleinere Schrift für Effekte, basierend auf der Basisgröße
        small_font = ImageFont.truetype("arialbd.ttf", int(base_font_size * 0.6))  # Kleinere Schrift für Effekte
         # Erstelle eine größere Schrift für Icons, basierend auf der Kartenhöhe
        icon_font = ImageFont.truetype("seguisym.ttf", int(card_height * 0.20))  # Größere Schrift für Symbole
    except IOError:
         # Wenn das Laden der Schriftart fehlschlägt, verwende eine Standardschriftart
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        icon_font = ImageFont.load_default()

    # Rufe die Funktion zum Erstellen des Ausgabeverzeichnisses auf
    output_dir = create_output_directory()

    # Iteriere durch jedes Element in der Liste der Elemente
    for element in elements:
        # Iteriere durch jeden Kartennamen in der Liste der Kartennamen
        for card_name in card_names:
            # Erstelle ein neues Bild mit der Größe der Karte und weißem Hintergrund
            card = Image.new("RGBA", (card_width, card_height), "white")
            # Erstelle ein Draw-Objekt, um auf dem Bild zu zeichnen
            draw = ImageDraw.Draw(card)

            # Zeichne einen Rahmen mit abgerundeten Ecken
            corner_radius = int(card_width * 0.05)  # Radius basierend auf Kartenbreite
            draw.rounded_rectangle(
                (15, 15, card_width - 15, card_height - 15),
                radius=corner_radius,
                outline="black",
                width=7  # Dickere Rahmen
            )

            # Definiere Farbverläufe für die Hintergründe der Karten, abhängig vom Element
            colors = {
                "Feuer": ("#FF5733", "#FFB37A"), # Dunkelrot zu Hellorange
                "Wasser": ("#3498DB", "#A7DDF2"), # Dunkelblau zu Hellblau
                "Erde": ("#7DCEA0", "#D4E7C4"), # Dunkelgrün zu Hellgrün
                "Luft": ("#F4D03F", "#FFF2CC"), # Dunkelgelb zu Hellgelb
                "Blitz": ("#F1C40F", "#FFF8B8"), # Dunkelgold zu Hellgold
                "Eis": ("#AED6F1", "#EAF2FC"), # Hellblau zu sehr Hellblau
                "Magie": ("#8E44AD", "#D2B4DE"), # Dunkelviolett zu Hellviolett
            }

             # Hole die Start- und Endfarbe für den Farbverlauf des aktuellen Elements
            start_color, end_color = colors.get(element, ("white", "white"))

            # Zeichne den Farbverlauf
            for i in range(card_height - 40):
                 # Wandle die Start- und Endfarbe in RGB-Werte um
                r_start, g_start, b_start = ImageColor.getrgb(start_color)
                r_end, g_end, b_end = ImageColor.getrgb(end_color)

                 # Berechne die interpolierten RGB-Werte für die aktuelle Zeile
                r = int(r_start + (r_end - r_start) * i / (card_height - 40))
                g = int(g_start + (g_end - g_start) * i / (card_height - 40))
                b = int(b_start + (b_end - b_start) * i / (card_height - 40))

                # Zeichne eine horizontale Linie mit der aktuellen Farbe
                draw.line([(20, 20 + i), (card_width - 20, 20 + i)], fill=(r, g, b))

            # Definiere Icons für jedes Element
            icons = {
                "Feuer": "🔥",
                "Wasser": "💧",
                "Erde": "🌱",
                "Luft": "🌬️",
                "Blitz": "⚡",
                "Eis": "🧊",
                "Magie": "✨",
            }

            # Hole das Icon für das aktuelle Element
            icon_text = icons.get(element, "?")
            
             # Berechne die Größe des Icons
            icon_width, icon_height = icon_font.getbbox(icon_text)[2:4]
             # Berechne die Position des Icons (zentriert)
            icon_x = (card_width - icon_width) // 2
            icon_y = int(card_height * 0.10)  # Positionierung basierend auf Kartenhöhe
             # Zeichne das Icon auf die Karte
            draw.text((icon_x, icon_y), icon_text, fill="black", font=icon_font)

            # Füge Text hinzu (Elementname und Kartenname)
            text = f"{element}\n{card_name}"
            # Teile den Text in Zeilen auf
            text_lines = text.split("\n")

            # Berechne die Gesamthöhe des Textblocks
            total_text_height = sum(font.getbbox(line)[3] for line in text_lines) + (len(text_lines) - 1) * 10
             # Berechne die Startposition für den Text
            current_y = icon_y + icon_height + int(card_height * 0.03)

            # Zeichne jede Textzeile zentriert
            for line in text_lines:
                text_width, text_height = font.getbbox(line)[2:4]
                text_x = (card_width - text_width) // 2
                draw.text((text_x, current_y), line, fill="black", font=font)
                current_y += text_height + int(card_height * 0.01)

            # Füge Effekte und Gewinninformationen hinzu
            effect_text = get_card_effect_text(element)
             # Teile den Text in Zeilen auf
            effect_lines = effect_text.split("\n")
            
             # Berechne die Gesamthöhe des Effekttextblocks
            total_effect_height = sum(small_font.getbbox(line)[3] for line in effect_lines) + (len(effect_lines) - 1) * int(card_height * 0.007)
            # Berechne die Startposition für den Effekttext (unten)
            current_y = card_height - int(card_height * 0.03) - total_effect_height

            # Zeichne jede Zeile des Effekttextes
            for line in effect_lines:
                text_width, text_height = small_font.getbbox(line)[2:4]
                text_x = (card_width - text_width) // 2
                draw.text((text_x, current_y), line, fill="black", font=small_font)
                current_y += text_height + int(card_height * 0.007)

            # Erstelle den Dateinamen für die Karte
            file_name = f"card_{element.lower()}_{card_name.lower()}.png"
             # Erstelle den vollständigen Dateipfad
            file_path = os.path.join(output_dir, file_name)

            # Speichere die Karte als PNG-Datei
            card.save(file_path, "PNG")

    # Gib eine Bestätigung aus, dass alle Karten erstellt wurden
    print(f"Alle Karten wurden im Verzeichnis '{output_dir}' erstellt.")

# Funktion zum Abrufen des Effekttextes für eine bestimmte Karte
def get_card_effect_text(element):
    """
    Gibt den Effekttext für das angegebene Element zurück.

    Args:
        element (str): Das Element, für das der Effekttext abgerufen werden soll.

    Returns:
        str: Der Effekttext für das angegebene Element.
    """
    # Definiere Effekte für jedes Element in einem Dictionary
    effects = {
        "Feuer": "Gewinn: gegen Erde\nVerlust: gegen Wasser\nEffekt: -1 Gegnertoken\n-1 Spielertoken",
        "Wasser": "Gewinn: gegen Feuer\nVerlust: gegen Luft\nEffekt: +1 Spielertoken\n-1 Gegnertoken\n+1 Gegnertoken\n-1 Spielertoken",
        "Erde": "Gewinn: gegen Blitz\nVerlust: gegen Feuer\nEffekt: +1 Spielertoken\n+1 Gegnertoken",
        "Luft": "Gewinn: gegen Wasser\nVerlust: gegen Blitz\nEffekt: +2 Spielertoken\n+2 Gegnertoken",
        "Blitz": "Gewinn: gegen Luft\nVerlust: gegen Erde\nEffekt: 2x Angriff",
        "Eis": "Gewinn: gegen Magie\nVerlust: gegen Blitz\nEffekt: Gegnerische\nKarten einfrieren",
        "Magie": "Gewinn: gegen Eis\nVerlust: gegen alle\nEffekt: Karten\nneu mischen",
    }
    # Gib den Effekttext für das angegebene Element zurück, oder "Kein Effekt" falls nicht gefunden
    return effects.get(element, "Kein Effekt")

# Hauptausführung des Skripts
if __name__ == "__main__":
    # Rufe die Funktion zum Erstellen der Kartenbilder auf
    create_card_images()
