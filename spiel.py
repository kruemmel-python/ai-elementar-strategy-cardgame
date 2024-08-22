import os  # Importiert das os-Modul für Betriebssystemoperationen.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Unterdrückt unnötige TensorFlow-Ausgaben in der Konsole.

import random  # Importiert das random-Modul für die Generierung von Zufallszahlen.
import pandas as pd  # Importiert Pandas zur Arbeit mit Daten in Tabellenform.
from tensorflow.keras.models import load_model  # Importiert die Funktion zum Laden eines Keras-Modells.
from sklearn.preprocessing import LabelEncoder  # Importiert den LabelEncoder, um kategorische Daten in numerische Werte umzuwandeln.
import numpy as np  # Importiert NumPy für numerische Operationen und die Arbeit mit Arrays.

# Definition der Karten und Elemente
ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft"]  # Definiert die vier Elemente im Spiel.
WERTE = ["1", "2","3", "4", "5", "6","7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]  # Definiert die möglichen Werte der Karten.

# Hierarchie der Elemente, um zu bestimmen, welches Element welches schlägt.
ELEMENT_HIERARCHIE = {
    "Wasser": "Feuer",  # Wasser schlägt Feuer.
    "Feuer": "Erde",    # Feuer schlägt Erde.
    "Erde": "Luft",     # Erde schlägt Luft.
    "Luft": "Wasser"    # Luft schlägt Wasser.
}

# ANSI-Farbcodes für die farbige Darstellung in der Konsole
FARBE_SPIELER = "\033[96m"  # Cyan für Spieleraktionen.
FARBE_KI = "\033[93m"  # Gelb für KI-Aktionen.
FARBE_GEWINNER_SPIELER = "\033[92m"  # Grün, wenn der Spieler gewinnt.
FARBE_GEWINNER_KI = "\033[91m"  # Rot, wenn die KI gewinnt.
FARBE_STAND = "\033[97m"  # Weiß für allgemeine Informationen und Spielstände.
FARBE_RESET = "\033[0m"  # Setzt die Farbe zurück auf die Standardfarbe.

# LabelEncoder für die Karten und Gewinner, um sie in numerische Werte umzuwandeln, die das Modell versteht.
label_encoder_karten = LabelEncoder()
label_encoder_karten.fit([f"{element} {wert}" for element in ELEMENTE for wert in WERTE])

# Laden des zuvor trainierten KI-Modells
modell_pfad = "Simulationen/elementar_schlacht_modell.keras"
modell = load_model(modell_pfad)  # Das Modell wird geladen, um Vorhersagen treffen zu können.

def deck_generieren():
    """
    Generiert ein gemischtes Kartendeck.

    Returns:
        list: Ein gemischtes Deck von Karten, wobei jede Karte eine Kombination aus Element und Wert ist.
    """
    deck = [(element, wert) for element in ELEMENTE for wert in WERTE]  # Erstellt das Deck durch Kombination der Elemente und Werte.
    random.shuffle(deck)  # Mischt das Deck, um die Reihenfolge der Karten zufällig zu machen.
    return deck  # Gibt das gemischte Deck zurück.

def bestimme_gewinner(spieler_karte, gegner_karte):
    """
    Bestimmt den Gewinner eines Schlages basierend auf den Werten der Karten und der Element-Hierarchie.

    Args:
        spieler_karte (tuple): Die Karte des Spielers als (Element, Wert).
        gegner_karte (tuple): Die Karte des Gegners als (Element, Wert).

    Returns:
        str: Der Gewinner des Schlages ("spieler", "gegner" oder "unentschieden").
    """
    spieler_element, spieler_wert = spieler_karte
    gegner_element, gegner_wert = gegner_karte

    spieler_wert_index = WERTE.index(spieler_wert)
    gegner_wert_index = WERTE.index(gegner_wert)

    # Vergleich der Elemente, wenn sie unterschiedlich sind
    if spieler_element != gegner_element:
        if ELEMENT_HIERARCHIE[spieler_element] == gegner_element:
            # Spieler-Element ist schwächer, könnte aber aufgrund des Wertes gewinnen.
            if spieler_wert_index < 4 and gegner_wert_index > 4:  # Spieler-Zahl < 5, Gegner-Zahl > 5
                return "gegner"
            elif spieler_wert_index > 4 and gegner_wert_index < 4:  # Spieler-Zahl > 5, Gegner-Zahl < 5
                return "spieler"
            else:
                return "gegner"  # Normalerweise gewinnt das stärkere Element.
        elif ELEMENT_HIERARCHIE[gegner_element] == spieler_element:
            # Gegner-Element ist schwächer, könnte aber aufgrund des Wertes gewinnen.
            if gegner_wert_index < 4 and spieler_wert_index > 4:  # Gegner-Zahl < 5, Spieler-Zahl > 5
                return "spieler"
            elif gegner_wert_index > 4 and spieler_wert_index < 4:  # Gegner-Zahl > 5, Spieler-Zahl < 5
                return "gegner"
            else:
                return "spieler"  # Normalerweise gewinnt das stärkere Element.
        else:
            if spieler_wert_index > gegner_wert_index:
                return "spieler"  # Spieler gewinnt, wenn sein Kartenwert höher ist.
            elif gegner_wert_index > spieler_wert_index:
                return "gegner"  # Gegner gewinnt, wenn sein Kartenwert höher ist.
            else:
                return "unentschieden"  # Es ist ein Unentschieden, wenn beide Karten gleich hoch sind.
    else:
        # Wenn die Elemente gleich sind, gewinnt die Karte mit dem höheren Wert.
        if spieler_wert_index > gegner_wert_index:
            return "spieler"
        elif gegner_wert_index > spieler_wert_index:
            return "gegner"
        else:
            return "unentschieden"

def wende_element_effekt_an(winner, element, spieler_token, gegner_token, spieler_hand, gegner_hand, talon):
    """
    Wendet die Effekte des Elements an, basierend auf dem Gewinner des Schlages.

    Args:
        winner (str): Der Gewinner des Schlages ("spieler" oder "gegner").
        element (str): Das Element der Karte, die den Schlag gewonnen hat.
        spieler_token (int): Die aktuelle Anzahl der Tokens des Spielers.
        gegner_token (int): Die aktuelle Anzahl der Tokens des Gegners.
        spieler_hand (list): Die aktuelle Hand des Spielers.
        gegner_hand (list): Die aktuelle Hand des Gegners.
        talon (list): Der Stapel der verbleibenden Karten.

    Returns:
        tuple: Die aktualisierte Anzahl der Tokens für Spieler und Gegner.
    """
    print(f"{FARBE_STAND}Vor dem Effekt: Spieler-Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")
    if element == "Feuer" and winner == "spieler":
        gegner_token -= 1  # Feuer reduziert die Tokens des Gegners um 1.
    elif element == "Wasser" and winner == "spieler":
        spieler_token += 1  # Wasser erhöht die Tokens des Spielers um 1.
        gegner_token -= 1  # Wasser reduziert die Tokens des Gegners um 1.
    elif element == "Erde" and winner == "spieler":
        spieler_token += 1  # Erde erhöht die Tokens des Spielers um 1.
    elif element == "Luft" and winner == "spieler":
        spieler_token += 2  # Luft gibt dem Spieler 2 zusätzliche Tokens.
        print(f"{FARBE_SPIELER}Du erhältst 2 zusätzliche Tokens!{FARBE_RESET}")
    elif element == "Feuer" and winner == "gegner":
        spieler_token -= 1  # Feuer reduziert die Tokens des Spielers um 1.
    elif element == "Wasser" and winner == "gegner":
        gegner_token += 1  # Wasser erhöht die Tokens des Gegners um 1.
        spieler_token -= 1  # Wasser reduziert die Tokens des Spielers um 1.
    elif element == "Erde" and winner == "gegner":
        gegner_token += 1  # Erde erhöht die Tokens des Gegners um 1.
    elif element == "Luft" and winner == "gegner":
        gegner_token += 2  # Luft gibt der KI 2 zusätzliche Tokens.
        print(f"{FARBE_KI}Die KI erhält 2 zusätzliche Tokens!{FARBE_RESET}")
    print(f"{FARBE_STAND}Nach dem Effekt: Spieler-Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")
    return spieler_token, gegner_token

def ki_waehlt_karte(gegner_hand, spieler_karte, spieler_token, gegner_token):
    """
    Wählt die beste Karte für die KI basierend auf dem Modell.

    Args:
        gegner_hand (list): Die aktuelle Hand der KI.
        spieler_karte (tuple): Die Karte, die der Spieler gespielt hat.
        spieler_token (int): Die aktuelle Anzahl der Tokens des Spielers.
        gegner_token (int): Die aktuelle Anzahl der Tokens der KI.

    Returns:
        tuple: Die Karte, die die KI spielen wird.
    """
    beste_karte = None
    beste_wahrscheinlichkeit = -1

    for gegner_karte in gegner_hand:
        spieler_karte_code = label_encoder_karten.transform([f"{spieler_karte[0]} {spieler_karte[1]}"])[0]
        gegner_karte_code = label_encoder_karten.transform([f"{gegner_karte[0]} {gegner_karte[1]}"])[0]

        features = np.array([[spieler_karte_code, gegner_karte_code, spieler_token, gegner_token]])

        vorhersage = modell.predict(features)
        wahrscheinlichkeit = vorhersage[0][0]

        if wahrscheinlichkeit > beste_wahrscheinlichkeit:
            beste_wahrscheinlichkeit = wahrscheinlichkeit
            beste_karte = gegner_karte

    return beste_karte  # Gibt die beste Karte zurück, die die KI spielen sollte.

def spiele_gegen_ki():
    """
    Startet ein Spiel gegen die KI, indem der Spieler und die KI abwechselnd Karten spielen.
    Das Spiel endet, wenn einer der Spieler keine Tokens mehr hat oder keine Karten mehr übrig sind.
    """
    deck = deck_generieren()  # Generiert ein gemischtes Deck.
    spieler_hand = deck[:4]  # Die ersten 4 Karten gehen an den Spieler.
    gegner_hand = deck[4:8]  # Die nächsten 4 Karten gehen an die KI.
    talon = deck[8:]  # Der Rest bildet den Stapel für die verbleibenden Karten (Talon).

    spieler_token = 2  # Der Spieler startet mit 5 Tokens.
    gegner_token = 2  # Die KI startet mit 5 Tokens.

    while spieler_token > 0 and gegner_token > 0 and (spieler_hand or gegner_hand):
        # Zeigt den aktuellen Spielstand an.
        print(f"{FARBE_STAND}\nDeine Karten: {spieler_hand}{FARBE_RESET}")
        print(f"{FARBE_STAND}Deine Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")

        if not spieler_hand:  # Überprüft, ob der Spieler noch Karten hat.
            print(f"{FARBE_STAND}Du hast keine Karten mehr.{FARBE_RESET}")
            break

        while True:
            try:
                # Spieler wählt eine Karte durch Eingabe der Indexposition.
                karten_auswahl = int(input(f"{FARBE_SPIELER}Wähle eine Karte (1-{len(spieler_hand)}): {FARBE_RESET}")) - 1
                if 0 <= karten_auswahl < len(spieler_hand):
                    spieler_karte = spieler_hand.pop(karten_auswahl)
                    break
                else:
                    print(f"{FARBE_SPIELER}Ungültige Auswahl.{FARBE_RESET}")
            except ValueError:
                print(f"{FARBE_SPIELER}Ungültige Eingabe. Bitte eine Zahl eingeben.{FARBE_RESET}")

        if gegner_hand:  # Überprüft, ob die KI noch Karten hat.
            gegner_karte = ki_waehlt_karte(gegner_hand, spieler_karte, spieler_token, gegner_token)
            gegner_hand.remove(gegner_karte)
            print(f"{FARBE_KI}KI spielt: {gegner_karte}{FARBE_RESET}")
        else:
            print(f"{FARBE_KI}Die KI hat keine Karten mehr.{FARBE_RESET}")
            break

        winner = bestimme_gewinner(spieler_karte, gegner_karte)
        if winner == "spieler":
            print(f"{FARBE_GEWINNER_SPIELER}Der Gewinner des Schlages ist: {winner}{FARBE_RESET}")
        elif winner == "gegner":
            print(f"{FARBE_GEWINNER_KI}Der Gewinner des Schlages ist: {winner}{FARBE_RESET}")
        else:
            print(f"{FARBE_STAND}Der Schlag endet unentschieden.{FARBE_RESET}")

        # Anwenden der Effekte basierend auf dem Element der Karte.
        spieler_token, gegner_token = wende_element_effekt_an(
            winner, spieler_karte[0], spieler_token, gegner_token, spieler_hand, gegner_hand, talon
        )

        if talon:  # Karten nachziehen, wenn noch Karten im Talon sind.
            if len(spieler_hand) < 4 and talon:
                spieler_hand.append(talon.pop())
            if len(gegner_hand) < 4 and talon:
                gegner_hand.append(talon.pop())

        # Zeigt die aktualisierte Hand des Spielers an.
        print(f"{FARBE_STAND}\nDeine aktualisierten Karten: {spieler_hand}{FARBE_RESET}")

    # Spielende
    if spieler_token > gegner_token:
        print(f"{FARBE_GEWINNER_SPIELER}\nGlückwunsch! Du hast gegen die KI gewonnen!{FARBE_RESET}")
    elif gegner_token > spieler_token:
        print(f"{FARBE_GEWINNER_KI}\nDie KI hat gewonnen. Versuch es noch einmal!{FARBE_RESET}")
    else:
        print(f"{FARBE_STAND}\nDas Spiel endet in einem Unentschieden.{FARBE_RESET}")

if __name__ == "__main__":
    spiele_gegen_ki()  # Startet das Spiel gegen die KI.
