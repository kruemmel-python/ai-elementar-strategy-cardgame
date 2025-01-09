from PIL import Image, ImageDraw, ImageFont, ImageColor
import os

# Verzeichnis für die Karten erstellen
def create_output_directory():
    output_dir = "karten_bilder"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir

# Kartenbilder erstellen
def create_card_images():
    # Liste der Elemente
    elements = ["Feuer", "Wasser", "Erde", "Luft", "Blitz", "Eis", "Magie"]

    # Kartennamen
    card_names = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Bube", "Dame", "Koenig", "Ass"
    ]

    # Größe der Karten
    card_width, card_height = 500, 700

    # Schriftart festlegen (dynamische Größe)
    try:
        base_font_size = int(card_height * 0.08)  # Basisschriftgröße, proportional zur Kartenhöhe
        font = ImageFont.truetype("arialbd.ttf", base_font_size)
        small_font = ImageFont.truetype("arialbd.ttf", int(base_font_size * 0.6))  # Kleinere Schrift für Effekte
        icon_font = ImageFont.truetype("seguisym.ttf", int(card_height * 0.20))  # Größere Schrift für Symbole
    except IOError:
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
        icon_font = ImageFont.load_default()

    # Verzeichnis für die Kartenbilder
    output_dir = create_output_directory()

    for element in elements:
        for card_name in card_names:
            # Bild erstellen
            card = Image.new("RGBA", (card_width, card_height), "white")
            draw = ImageDraw.Draw(card)

            # Rahmen zeichnen (mit abgerundeten Ecken)
            corner_radius = int(card_width * 0.05)  # Radius basierend auf Kartenbreite
            draw.rounded_rectangle(
                (15, 15, card_width - 15, card_height - 15),
                radius=corner_radius,
                outline="black",
                width=7  # Dickere Rahmen
            )

            # Hintergrundfarbe basierend auf Element (mit Farbverlauf)
            colors = {
                "Feuer": ("#FF5733", "#FFB37A"),
                "Wasser": ("#3498DB", "#A7DDF2"),
                "Erde": ("#7DCEA0", "#D4E7C4"),
                "Luft": ("#F4D03F", "#FFF2CC"),
                "Blitz": ("#F1C40F", "#FFF8B8"),
                "Eis": ("#AED6F1", "#EAF2FC"),
                "Magie": ("#8E44AD", "#D2B4DE"),
            }

            start_color, end_color = colors.get(element, ("white", "white"))

            # Farbverlauf malen
            for i in range(card_height - 40):
                r_start, g_start, b_start = ImageColor.getrgb(start_color)
                r_end, g_end, b_end = ImageColor.getrgb(end_color)

                r = int(r_start + (r_end - r_start) * i / (card_height - 40))
                g = int(g_start + (g_end - g_start) * i / (card_height - 40))
                b = int(b_start + (b_end - b_start) * i / (card_height - 40))

                draw.line([(20, 20 + i), (card_width - 20, 20 + i)], fill=(r, g, b))

            # Element Icon hinzufügen
            icons = {
                "Feuer": "🔥",
                "Wasser": "💧",
                "Erde": "🌱",
                "Luft": "🌬️",
                "Blitz": "⚡",
                "Eis": "🧊",
                "Magie": "✨",
            }

            icon_text = icons.get(element, "?")
            
            icon_width, icon_height = icon_font.getbbox(icon_text)[2:4]
            icon_x = (card_width - icon_width) // 2
            icon_y = int(card_height * 0.10) # Positionierung basierend auf Kartenhöhe
            draw.text((icon_x, icon_y), icon_text, fill="black", font=icon_font)

            # Text hinzufügen (Elementname und Kartenname)
            text = f"{element}\n{card_name}"
            text_lines = text.split("\n")

            # Position des Textes berechnen (zentriert unter dem Icon)
            total_text_height = sum(font.getbbox(line)[3] for line in text_lines) + (len(text_lines) - 1) * 10
            current_y = icon_y + icon_height + int(card_height * 0.03)

            for line in text_lines:
                text_width, text_height = font.getbbox(line)[2:4]
                text_x = (card_width - text_width) // 2
                draw.text((text_x, current_y), line, fill="black", font=font)
                current_y += text_height + int(card_height * 0.01)

             # Effekte und Gewinninfos hinzufügen
            effect_text = get_card_effect_text(element)
            effect_lines = effect_text.split("\n")
            
            total_effect_height = sum(small_font.getbbox(line)[3] for line in effect_lines) + (len(effect_lines) - 1) * int(card_height * 0.007)
            current_y = card_height - int(card_height * 0.03) - total_effect_height

            for line in effect_lines:
                text_width, text_height = small_font.getbbox(line)[2:4]
                text_x = (card_width - text_width) // 2
                draw.text((text_x, current_y), line, fill="black", font=small_font)
                current_y += text_height + int(card_height * 0.007)

            # Dateiname erstellen
            file_name = f"card_{element.lower()}_{card_name.lower()}.png"
            file_path = os.path.join(output_dir, file_name)

            # Bild speichern
            card.save(file_path, "PNG")

    print(f"Alle Karten wurden im Verzeichnis '{output_dir}' erstellt.")

def get_card_effect_text(element):
    effects = {
        "Feuer": "Gewinn: gegen Erde\nVerlust: gegen Wasser\nEffekt: -1 Gegnertoken\n-1 Spielertoken",
        "Wasser": "Gewinn: gegen Feuer\nVerlust: gegen Luft\nEffekt: +1 Spielertoken\n-1 Gegnertoken\n+1 Gegnertoken\n-1 Spielertoken",
        "Erde": "Gewinn: gegen Blitz\nVerlust: gegen Feuer\nEffekt: +1 Spielertoken\n+1 Gegnertoken",
        "Luft": "Gewinn: gegen Wasser\nVerlust: gegen Blitz\nEffekt: +2 Spielertoken\n+2 Gegnertoken",
         "Blitz": "Gewinn: gegen Luft\nVerlust: gegen Erde\nEffekt: 2x Angriff",
        "Eis": "Gewinn: gegen Magie\nVerlust: gegen Blitz\nEffekt: Gegnerische\nKarten einfrieren",
        "Magie": "Gewinn: gegen Eis\nVerlust: gegen alle\nEffekt: Karten\nneu mischen",
    }
    return effects.get(element, "Kein Effekt")


if __name__ == "__main__":
    create_card_images()