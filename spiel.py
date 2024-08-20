import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # TensorFlow-Ausgaben unterdrücken

import random
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Definition der Karten und Elemente
ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft"]
WERTE = ["7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]

# Hierarchie der Elemente
ELEMENT_HIERARCHIE = {
    "Wasser": "Feuer",  # Wasser schlägt Feuer
    "Feuer": "Erde",    # Feuer schlägt Erde
    "Erde": "Luft",     # Erde schlägt Luft
    "Luft": "Wasser"    # Luft schlägt Wasser
}

# ANSI-Farbcodes
FARBE_SPIELER = "\033[96m"  # Cyan für Spieleraktionen
FARBE_KI = "\033[93m"  # Gelb für KI-Aktionen
FARBE_GEWINNER_SPIELER = "\033[92m"  # Grün für Spieler, wenn er gewinnt
FARBE_GEWINNER_KI = "\033[91m"  # Rot für KI, wenn sie gewinnt
FARBE_STAND = "\033[97m"  # Weiß für Spielstände und allgemeine Informationen
FARBE_RESET = "\033[0m"  # Zurücksetzen der Farbe

# LabelEncoder für die Karten und Gewinner (damit die KI das versteht)
label_encoder_karten = LabelEncoder()
label_encoder_karten.fit([f"{element} {wert}" for element in ELEMENTE for wert in WERTE])

# Laden des KI-Modells
modell_pfad = "Simulationen/elementar_schlacht_modell.keras"
modell = load_model(modell_pfad)

# Funktion zur Generierung eines Decks
def deck_generieren():
    deck = [(element, wert) for element in ELEMENTE for wert in WERTE]
    random.shuffle(deck)
    return deck

# Funktion zur Bestimmung des Gewinners eines Schlages unter Berücksichtigung der Element-Hierarchie
def bestimme_gewinner(spieler_karte, gegner_karte):
    spieler_element, spieler_wert = spieler_karte
    gegner_element, gegner_wert = gegner_karte

    # Bestimme die Indexe der Werte
    spieler_wert_index = WERTE.index(spieler_wert)
    gegner_wert_index = WERTE.index(gegner_wert)

    # Wenn die Elemente unterschiedlich sind, prüfe die Hierarchie
    if spieler_element != gegner_element:
        if ELEMENT_HIERARCHIE[spieler_element] == gegner_element:
            # Spieler-Element ist schwächer, aber möglicherweise gewinnt es aufgrund der Zahl
            if spieler_wert_index < 4 and gegner_wert_index > 4:  # Spieler-Zahl < 5, Gegner-Zahl > 5
                return "gegner"
            elif spieler_wert_index > 4 and gegner_wert_index < 4:  # Spieler-Zahl > 5, Gegner-Zahl < 5
                return "spieler"
            else:
                return "gegner"  # Normalerweise würde das stärkere Element gewinnen
        elif ELEMENT_HIERARCHIE[gegner_element] == spieler_element:
            # Gegner-Element ist schwächer, aber möglicherweise gewinnt es aufgrund der Zahl
            if gegner_wert_index < 4 and spieler_wert_index > 4:  # Gegner-Zahl < 5, Spieler-Zahl > 5
                return "spieler"
            elif gegner_wert_index > 4 and spieler_wert_index < 4:  # Gegner-Zahl > 5, Spieler-Zahl < 5
                return "gegner"
            else:
                return "spieler"  # Normalerweise würde das stärkere Element gewinnen
        else:
            # Wenn keines der beiden Elemente dominiert, gewinnt das Element mit der höheren Zahl
            if spieler_wert_index > gegner_wert_index:
                return "spieler"
            elif gegner_wert_index > spieler_wert_index:
                return "gegner"
            else:
                return "unentschieden"
    else:
        # Wenn die Elemente gleich sind, gewinnt die höhere Zahl
        if spieler_wert_index > gegner_wert_index:
            return "spieler"
        elif gegner_wert_index > spieler_wert_index:
            return "gegner"
        else:
            return "unentschieden"

# Funktion zur Anwendung der Element-Effekte
def wende_element_effekt_an(winner, element, spieler_token, gegner_token, spieler_hand, gegner_hand, talon):
    print(f"{FARBE_STAND}Vor dem Effekt: Spieler-Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")
    if element == "Feuer" and winner == "spieler":
        gegner_token -= 1
    elif element == "Wasser" and winner == "spieler":
        spieler_token += 1
        gegner_token -= 1
    elif element == "Erde" and winner == "spieler":
        spieler_token += 1
    elif element == "Luft" and winner == "spieler":
        spieler_token += 2  # Spieler erhält 2 zusätzliche Tokens
        print(f"{FARBE_SPIELER}Du erhältst 2 zusätzliche Tokens!{FARBE_RESET}")
    elif element == "Feuer" and winner == "gegner":
        spieler_token -= 1
    elif element == "Wasser" and winner == "gegner":
        gegner_token += 1
        spieler_token -= 1
    elif element == "Erde" and winner == "gegner":
        gegner_token += 1
    elif element == "Luft" and winner == "gegner":
        gegner_token += 2  # Gegner erhält 2 zusätzliche Tokens
        print(f"{FARBE_KI}Die KI erhält 2 zusätzliche Tokens!{FARBE_RESET}")
    print(f"{FARBE_STAND}Nach dem Effekt: Spieler-Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")
    return spieler_token, gegner_token

# Funktion zur Auswahl der besten KI-Karte
def ki_waehlt_karte(gegner_hand, spieler_karte, spieler_token, gegner_token):
    beste_karte = None
    beste_wahrscheinlichkeit = -1

    for gegner_karte in gegner_hand:
        # Kodierung der Karten in Features für das Modell
        spieler_karte_code = label_encoder_karten.transform([f"{spieler_karte[0]} {spieler_karte[1]}"])[0]
        gegner_karte_code = label_encoder_karten.transform([f"{gegner_karte[0]} {gegner_karte[1]}"])[0]

        # Erstellen der Feature-Matrix für die Vorhersage
        features = np.array([[spieler_karte_code, gegner_karte_code, spieler_token, gegner_token]])

        # Vorhersage des Modells
        vorhersage = modell.predict(features)
        wahrscheinlichkeit = vorhersage[0][0]  # Wahrscheinlichkeit, dass der Spieler gewinnt

        if wahrscheinlichkeit > beste_wahrscheinlichkeit:
            beste_wahrscheinlichkeit = wahrscheinlichkeit
            beste_karte = gegner_karte

    return beste_karte

# Funktion, um ein Spiel gegen die KI zu spielen
def spiele_gegen_ki():
    deck = deck_generieren()
    spieler_hand = deck[:4]
    gegner_hand = deck[4:8]
    talon = deck[8:]

    spieler_token = 5
    gegner_token = 5

    while spieler_token > 0 and gegner_token > 0 and (spieler_hand or gegner_hand):
        # Spielstand anzeigen
        print(f"{FARBE_STAND}\nDeine Karten: {spieler_hand}{FARBE_RESET}")
        print(f"{FARBE_STAND}Deine Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")

        # Überprüfen, ob der Spieler Karten hat
        if not spieler_hand:
            print(f"{FARBE_STAND}Du hast keine Karten mehr.{FARBE_RESET}")
            break

        # Spieler wählt eine Karte
        while True:
            try:
                karten_auswahl = int(input(f"{FARBE_SPIELER}Wähle eine Karte (1-{len(spieler_hand)}): {FARBE_RESET}")) - 1
                if 0 <= karten_auswahl < len(spieler_hand):
                    spieler_karte = spieler_hand.pop(karten_auswahl)
                    break
                else:
                    print(f"{FARBE_SPIELER}Ungültige Auswahl.{FARBE_RESET}")
            except ValueError:
                print(f"{FARBE_SPIELER}Ungültige Eingabe. Bitte eine Zahl eingeben.{FARBE_RESET}")

        # KI wählt eine Karte
        if gegner_hand:  # Überprüfen, ob die KI noch Karten hat
            gegner_karte = ki_waehlt_karte(gegner_hand, spieler_karte, spieler_token, gegner_token)
            gegner_hand.remove(gegner_karte)
            print(f"{FARBE_KI}KI spielt: {gegner_karte}{FARBE_RESET}")
        else:
            print(f"{FARBE_KI}Die KI hat keine Karten mehr.{FARBE_RESET}")
            break

        # Bestimme den Gewinner des Schlages
        winner = bestimme_gewinner(spieler_karte, gegner_karte)
        if winner == "spieler":
            print(f"{FARBE_GEWINNER_SPIELER}Der Gewinner des Schlages ist: {winner}{FARBE_RESET}")
        else:
            print(f"{FARBE_GEWINNER_KI}Der Gewinner des Schlages ist: {winner}{FARBE_RESET}")

        # Anwenden des Effekts basierend auf dem Element der Karte
        spieler_token, gegner_token = wende_element_effekt_an(
            winner, spieler_karte[0], spieler_token, gegner_token, spieler_hand, gegner_hand, talon
        )

        # Karten nachziehen, wenn noch Karten im Talon sind
        if talon:
            if len(spieler_hand) < 4:
                spieler_hand.append(talon.pop())
            if len(gegner_hand) < 4:
                gegner_hand.append(talon.pop())

        # Aktualisierte Hand des Spielers anzeigen
        print(f"{FARBE_STAND}\nDeine aktualisierten Karten: {spieler_hand}{FARBE_RESET}")

    # Spielende
    if spieler_token > 0 and not gegner_hand:
        print(f"{FARBE_GEWINNER_SPIELER}\nGlückwunsch! Du hast gegen die KI gewonnen!{FARBE_RESET}")
    elif gegner_token > 0 and not spieler_hand:
        print(f"{FARBE_GEWINNER_KI}\nDie KI hat gewonnen. Versuch es noch einmal!{FARBE_RESET}")
    else:
        print(f"{FARBE_STAND}\nDas Spiel endet in einem Unentschieden.{FARBE_RESET}")

# Spiel starten
if __name__ == "__main__":
    spiele_gegen_ki()
