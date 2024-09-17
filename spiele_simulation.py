import csv  # Importiert das Modul zum Arbeiten mit CSV-Dateien.
import random  # Importiert das Modul zur Generierung von Zufallszahlen und zufälligen Auswahlmöglichkeiten.

# Definition der Karten, Elemente, Helden und Artefakte
ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft", "Blitz", "Eis", "Magie"]
WERTE = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]
ANZAHL_ELEMENTAR_PUNKTE = 5
HELDEN = ["Drache", "Zauberer"]
ARTEFAKTE = ["Zauberstab"]

# Wettereffekte
WETTEREFFEKT = {"Regen": {"Wasser": 1, "Feuer": -1}, "Windsturm": {"Luft": 2, "Erde": -1}, "Erdbeben": {}}

def deck_generieren():
    deck = [(element, wert) for element in ELEMENTE for wert in WERTE]
    random.shuffle(deck)
    return deck

def zufaelliges_wetter():
    wetter = random.choice(list(WETTEREFFEKT.keys()))
    return wetter, WETTEREFFEKT[wetter]

def bestimme_gewinner(spieler_karte, gegner_karte, spieler_token, gegner_token, wettereffekt):
    spieler_element, spieler_wert = spieler_karte
    gegner_element, gegner_wert = gegner_karte
    spieler_wert_index = WERTE.index(spieler_wert)
    gegner_wert_index = WERTE.index(gegner_wert)

    # Elementboni basierend auf dem Wettereffekt hinzufügen
    spieler_bonus = wettereffekt.get(spieler_element, 0)
    gegner_bonus = wettereffekt.get(gegner_element, 0)

    # Vergleich basierend auf Kartenwert und Boni
    gesamtwert_spieler = spieler_wert_index + spieler_bonus
    gesamtwert_gegner = gegner_wert_index + gegner_bonus

    if gesamtwert_spieler > gesamtwert_gegner:
        return "spieler"
    elif gesamtwert_gegner > gesamtwert_spieler:
        return "gegner"
    else:
        return "unentschieden"

def wende_element_effekt_an(winner, element, spieler_token, gegner_token):
    """
    Wendet die Effekte des Elementes an, basierend auf dem Gewinner des Schlages.

    Args:
        winner (str): Der Gewinner des Schlages ("spieler" oder "gegner").
        element (str): Das Element der Karte, die den Schlag gewonnen hat.
        spieler_token (int): Die aktuelle Anzahl der Tokens des Spielers.
        gegner_token (int): Die aktuelle Anzahl der Tokens des Gegners.

    Returns:
        tuple: Die aktualisierte Anzahl der Tokens für Spieler und Gegner.
    """
    if element == "Feuer" and winner == "spieler":
        gegner_token -= 1  # Feuer verringert die Tokens des Gegners.
    elif element == "Wasser" and winner == "spieler":
        spieler_token += 1  # Wasser erhöht die Tokens des Spielers.
        gegner_token -= 1  # Wasser verringert die Tokens des Gegners.
    elif element == "Erde" and winner == "spieler":
        spieler_token += 1  # Erde erhöht die Tokens des Spielers.
    elif element == "Luft" and winner == "spieler":
        pass  # Luft hat in dieser Implementierung keinen Effekt.

    elif element == "Feuer" and winner == "gegner":
        spieler_token -= 1  # Feuer verringert die Tokens des Spielers.
    elif element == "Wasser" and winner == "gegner":
        gegner_token += 1  # Wasser erhöht die Tokens des Gegners.
        spieler_token -= 1  # Wasser verringert die Tokens des Spielers.
    elif element == "Erde" and winner == "gegner":
        gegner_token += 1  # Erde erhöht die Tokens des Gegners.
    elif element == "Luft" and winner == "gegner":
        pass  # Luft hat in dieser Implementierung keinen Effekt.

    return spieler_token, gegner_token  # Gibt die aktualisierten Token-Werte zurück.



def simuliere_spiel():
    deck = deck_generieren()
    spieler_hand = deck[:4]
    gegner_hand = deck[4:8]
    talon = deck[8:]
    spieler_token = ANZAHL_ELEMENTAR_PUNKTE
    gegner_token = ANZAHL_ELEMENTAR_PUNKTE
    spieler_held = random.choice(HELDEN)
    gegner_held = random.choice(HELDEN)
    spiel_daten = []

    while spieler_token > 0 and gegner_token > 0:
        wetter, wettereffekt = zufaelliges_wetter()

        if spieler_hand:  
            spieler_karte = random.choice(spieler_hand)
            spieler_hand.remove(spieler_karte)
        else:
            break

        if gegner_hand:  
            gegner_karte = random.choice(gegner_hand)
            gegner_hand.remove(gegner_karte)
        else:
            break

        # Bestimme den Gewinner unter Einbezug von Wetter und Helden
        winner = bestimme_gewinner(spieler_karte, gegner_karte, spieler_token, gegner_token, wettereffekt)
        spieler_token, gegner_token = wende_element_effekt_an(winner, spieler_karte[0], spieler_token, gegner_token)

        spiel_daten.append({
            "spieler_karte": f"{spieler_karte[0]} {spieler_karte[1]}",
            "gegner_karte": f"{gegner_karte[0]} {gegner_karte[1]}",
            "spieler_token": spieler_token,
            "gegner_token": gegner_token,
            "wetter": wetter,
            "spieler_held": spieler_held,
            "gegner_held": gegner_held,
            "gewinner": winner
        })

        if talon:
            if len(spieler_hand) < 4:
                spieler_hand.append(talon.pop())
            if len(gegner_hand) < 4:
                gegner_hand.append(talon.pop())

    return spiel_daten

def speichere_spieldaten_in_csv(spiel_daten, dateiname="Simulationen/spieldaten.csv"):
    schluessel = spiel_daten[0].keys()
    with open(dateiname, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=schluessel)
        writer.writeheader()
        writer.writerows(spiel_daten)

def generiere_und_speichere_spiele(anzahl_spiele=10000):
    alle_spiel_daten = []
    for _ in range(anzahl_spiele):
        spiel_daten = simuliere_spiel()
        alle_spiel_daten.extend(spiel_daten)
    speichere_spieldaten_in_csv(alle_spiel_daten)

# Beispielaufruf zur Generierung und Speicherung von 10.000 Spielen
generiere_und_speichere_spiele(10000)
