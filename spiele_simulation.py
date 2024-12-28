import csv
import random
from pathlib import Path
import logging

# Configure logging
LOG_DATEI = "simulationen.log"
logging.basicConfig(filename=LOG_DATEI, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define constants
ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft", "Blitz", "Eis", "Magie"]
WERTE = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]
ANZAHL_ELEMENTAR_PUNKTE = 5
HELDEN = ["Drache", "Zauberer"]
ARTEFAKTE = ["Zauberstab"]
WETTEREFFEKTE = {"Regen": {"Wasser": 1, "Feuer": -1}, "Windsturm": {"Luft": 2, "Erde": -1}, "Erdbeben": {}}
SIMULATIONEN_VERZEICHNIS = "Simulationen"
SPIELDATEN_DATEI = Path(SIMULATIONEN_VERZEICHNIS) / "spieldaten.csv"
ANZAHL_STARTHANDKARTEN = 4

def deck_generieren():
    """
    Generates a shuffled deck of cards consisting of elements and values.

    Returns:
        list: A list of tuples representing the shuffled deck of cards.
    """
    deck = [(element, wert) for element in ELEMENTE for wert in WERTE]
    random.shuffle(deck)
    logging.info("Neues Deck generiert.")
    return deck

def zufaelliges_wetter():
    """
    Randomly selects a weather event.

    Returns:
        tuple: A tuple containing the selected weather event and its effects.
    """
    wetter = random.choice(list(WETTEREFFEKTE.keys()))
    logging.info(f"Zufälliges Wetter gewählt: {wetter}")
    return wetter, WETTEREFFEKTE[wetter]

def bestimme_gewinner(spieler_karte, gegner_karte, wettereffekt):
    """
    Determines the winner of a battle based on card values and weather effects.

    Args:
        spieler_karte (tuple): The player's card.
        gegner_karte (tuple): The opponent's card.
        wettereffekt (dict): The weather effects.

    Returns:
        str: The winner of the battle ("spieler", "gegner", or "unentschieden").
    """
    spieler_element, spieler_wert = spieler_karte
    gegner_element, gegner_wert = gegner_karte
    spieler_wert_index = WERTE.index(spieler_wert)
    gegner_wert_index = WERTE.index(gegner_wert)

    spieler_bonus = wettereffekt.get(spieler_element, 0)
    gegner_bonus = wettereffekt.get(gegner_element, 0)

    gesamtwert_spieler = spieler_wert_index + spieler_bonus
    gesamtwert_gegner = gegner_wert_index + gegner_bonus

    if gesamtwert_spieler > gesamtwert_gegner:
        logging.debug(f"Spieler gewinnt mit {spieler_karte} (Gesamtwert: {gesamtwert_spieler}) gegen {gegner_karte} (Gesamtwert: {gesamtwert_gegner}).")
        return "spieler"
    elif gesamtwert_gegner > gesamtwert_spieler:
        logging.debug(f"Gegner gewinnt mit {gegner_karte} (Gesamtwert: {gesamtwert_gegner}) gegen {spieler_karte} (Gesamtwert: {gesamtwert_spieler}).")
        return "gegner"
    else:
        logging.debug(f"Unentschieden zwischen Spieler ({spieler_karte}, Gesamtwert: {gesamtwert_spieler}) und Gegner ({gegner_karte}, Gesamtwert: {gesamtwert_gegner}).")
        return "unentschieden"

def wende_element_effekt_an(gewinner, element, spieler_token, gegner_token):
    """
    Applies element effects based on the winner.

    Args:
        gewinner (str): The winner of the battle ("spieler" or "gegner").
        element (str): The element of the card.
        spieler_token (int): The player's elemental points.
        gegner_token (int): The opponent's elemental points.

    Returns:
        tuple: The updated elemental points for the player and the opponent.
    """
    effekte = {
        ("Feuer", "spieler"): lambda st, gt: (st, gt - 1),
        ("Wasser", "spieler"): lambda st, gt: (st + 1, gt - 1),
        ("Erde", "spieler"): lambda st, gt: (st + 1, gt),
        ("Luft", "spieler"): lambda st, gt: (st, gt),
        ("Feuer", "gegner"): lambda st, gt: (st - 1, gt),
        ("Wasser", "gegner"): lambda st, gt: (st - 1, gt + 1),
        ("Erde", "gegner"): lambda st, gt: (st, gt + 1),
        ("Luft", "gegner"): lambda st, gt: (st, gt),
    }
    if (element, gewinner) in effekte:
        spieler_token, gegner_token = effekte[(element, gewinner)](spieler_token, gegner_token)
        logging.debug(f"Elementeffekt von {element} angewendet. Spieler-Token: {spieler_token}, Gegner-Token: {gegner_token}")
    return spieler_token, gegner_token

def simuliere_spiel():
    """
    Simulates a single game.

    Returns:
        list: A list of dictionaries containing the game data for each turn.
    """
    deck = deck_generieren()
    spieler_hand = deck[:ANZAHL_STARTHANDKARTEN]
    gegner_hand = deck[ANZAHL_STARTHANDKARTEN:2 * ANZAHL_STARTHANDKARTEN]
    talon = deck[2 * ANZAHL_STARTHANDKARTEN:]
    spieler_token = ANZAHL_ELEMENTAR_PUNKTE
    gegner_token = ANZAHL_ELEMENTAR_PUNKTE
    spieler_held = random.choice(HELDEN)
    gegner_held = random.choice(HELDEN)
    spiel_daten = []

    logging.info(f"Starte ein neues Spiel. Spielerheld: {spieler_held}, Gegnerheld: {gegner_held}")

    while spieler_token > 0 and gegner_token > 0:
        wetter, wettereffekt = zufaelliges_wetter()

        if not spieler_hand or not gegner_hand:
            logging.info("Spiel beendet, da ein Spieler keine Karten mehr hat.")
            break

        spieler_karte = random.choice(spieler_hand)
        spieler_hand.remove(spieler_karte)
        gegner_karte = random.choice(gegner_hand)
        gegner_hand.remove(gegner_karte)

        gewinner = bestimme_gewinner(spieler_karte, gegner_karte, wettereffekt)
        spieler_token, gegner_token = wende_element_effekt_an(gewinner, spieler_karte[0], spieler_token, gegner_token)

        spiel_daten.append({
            "spieler_karte": f"{spieler_karte[0]} {spieler_karte[1]}",
            "gegner_karte": f"{gegner_karte[0]} {gegner_karte[1]}",
            "spieler_token": spieler_token,
            "gegner_token": gegner_token,
            "wetter": wetter,
            "spieler_held": spieler_held,
            "gegner_held": gegner_held,
            "gewinner": gewinner
        })

        if talon:
            if len(spieler_hand) < ANZAHL_STARTHANDKARTEN:
                spieler_hand.append(talon.pop())
            if len(gegner_hand) < ANZAHL_STARTHANDKARTEN:
                gegner_hand.append(talon.pop())

    logging.info(f"Spiel beendet. Spieler-Token: {spieler_token}, Gegner-Token: {gegner_token}")
    return spiel_daten

def speichere_spieldaten_in_csv(spiel_daten, dateiname):
    """
    Saves game data to a CSV file.

    Args:
        spiel_daten (list): A list of dictionaries containing the game data.
        dateiname (str): The name of the CSV file to save the data to.
    """
    schluessel = spiel_daten[0].keys()
    with open(dateiname, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=schluessel)
        writer.writeheader()
        writer.writerows(spiel_daten)
    logging.info(f"{len(spiel_daten)} Spielzüge in {dateiname} gespeichert.")

def generiere_und_speichere_spiele(anzahl_spiele=10000):
    """
    Generates multiple games and saves the data to a CSV file.

    Args:
        anzahl_spiele (int): The number of games to generate. Default is 10000.
    """
    Path(SIMULATIONEN_VERZEICHNIS).mkdir(parents=True, exist_ok=True)
    alle_spiel_daten = []
    logging.info(f"Starte die Generierung von {anzahl_spiele} Spielen.")
    for i in range(anzahl_spiele):
        spiel_daten = simuliere_spiel()
        alle_spiel_daten.extend(spiel_daten)
        logging.info(f"Spiel {i + 1}/{anzahl_spiele} simuliert.")
    speichere_spieldaten_in_csv(alle_spiel_daten, SPIELDATEN_DATEI)
    logging.info(f"Alle {anzahl_spiele} Spiele simuliert und Daten gespeichert.")

if __name__ == "__main__":
    generiere_und_speichere_spiele(10000)
