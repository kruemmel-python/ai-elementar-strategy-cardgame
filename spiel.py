import os  # Importiert das os-Modul, das für die Arbeit mit dem Betriebssystem erforderlich ist
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Unterdrückt TensorFlow-Ausgaben, um die Konsole sauberer zu halten

import random  # Wird verwendet, um Zufallszahlen und zufällige Auswahlmöglichkeiten zu generieren
import pandas as pd  # Bibliothek für die Arbeit mit Daten in Tabellenform (z.B. CSV-Dateien)
from tensorflow.keras.models import load_model  # Funktion zum Laden eines Keras-Modells
from sklearn.preprocessing import LabelEncoder  # Wird verwendet, um kategorische Daten in numerische Werte umzuwandeln
import numpy as np  # Bibliothek für numerische Berechnungen, insbesondere für Arrays

# Definition der Karten und Elemente
ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft"]  # Die vier Elemente, die im Spiel vorkommen
WERTE = ["7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]  # Die möglichen Werte der Karten

# Hierarchie der Elemente
# Diese Hierarchie bestimmt, welches Element stärker als ein anderes ist
ELEMENT_HIERARCHIE = {
    "Wasser": "Feuer",  # Wasser schlägt Feuer
    "Feuer": "Erde",    # Feuer schlägt Erde
    "Erde": "Luft",     # Erde schlägt Luft
    "Luft": "Wasser"    # Luft schlägt Wasser
}

# ANSI-Farbcodes für farbige Konsolenausgaben
FARBE_SPIELER = "\033[96m"  # Cyan für Spieleraktionen
FARBE_KI = "\033[93m"  # Gelb für KI-Aktionen
FARBE_GEWINNER_SPIELER = "\033[92m"  # Grün, wenn der Spieler gewinnt
FARBE_GEWINNER_KI = "\033[91m"  # Rot, wenn die KI gewinnt
FARBE_STAND = "\033[97m"  # Weiß für allgemeine Informationen und Spielstände
FARBE_RESET = "\033[0m"  # Setzt die Farbe zurück auf die Standardfarbe

# LabelEncoder für die Karten (um sie in numerische Werte zu konvertieren, die das KI-Modell versteht)
label_encoder_karten = LabelEncoder()
# Die Karten werden in numerische Werte umgewandelt, damit das Modell sie verarbeiten kann
label_encoder_karten.fit([f"{element} {wert}" for element in ELEMENTE for wert in WERTE])

# Laden des zuvor trainierten KI-Modells
modell_pfad = "Simulationen/elementar_schlacht_modell.keras"
modell = load_model(modell_pfad)  # Modell wird geladen und steht für Vorhersagen zur Verfügung

# Funktion zur Generierung eines Decks
def deck_generieren():
    # Das Deck wird erstellt, indem jede Kombination aus Element und Wert generiert wird
    deck = [(element, wert) for element in ELEMENTE for wert in WERTE]
    # Das Deck wird gemischt, um zufällige Kartenreihenfolgen zu erzeugen
    random.shuffle(deck)
    return deck

# Funktion zur Bestimmung des Gewinners eines Schlages unter Berücksichtigung der Element-Hierarchie
def bestimme_gewinner(spieler_karte, gegner_karte):
    # Extrahiert das Element und den Wert der Karten
    spieler_element, spieler_wert = spieler_karte
    gegner_element, gegner_wert = gegner_karte

    # Bestimmt die Indexe der Werte (z.B. Ass > König > Dame usw.)
    spieler_wert_index = WERTE.index(spieler_wert)
    gegner_wert_index = WERTE.index(gegner_wert)

    # Vergleich der Elemente, wenn sie unterschiedlich sind
    if spieler_element != gegner_element:
        if ELEMENT_HIERARCHIE[spieler_element] == gegner_element:
            # Spieler-Element ist schwächer, könnte aber gewinnen, wenn die Zahl groß genug ist
            if spieler_wert_index < 4 and gegner_wert_index > 4:  # Spieler-Zahl < 5, Gegner-Zahl > 5
                return "gegner"
            elif spieler_wert_index > 4 and gegner_wert_index < 4:  # Spieler-Zahl > 5, Gegner-Zahl < 5
                return "spieler"
            else:
                return "gegner"  # Normalerweise gewinnt das stärkere Element
        elif ELEMENT_HIERARCHIE[gegner_element] == spieler_element:
            # Gegner-Element ist schwächer, könnte aber gewinnen, wenn die Zahl groß genug ist
            if gegner_wert_index < 4 und spieler_wert_index > 4:  # Gegner-Zahl < 5, Spieler-Zahl > 5
                return "spieler"
            elif gegner_wert_index > 4 and spieler_wert_index < 4:  # Gegner-Zahl > 5, Spieler-Zahl < 5
                return "gegner"
            else:
                return "spieler"  # Normalerweise gewinnt das stärkere Element
        else:
            # Wenn keines der beiden Elemente dominiert, gewinnt die höhere Zahl
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

# Funktion zur Anwendung der Element-Effekte nach einem gewonnenen Schlag
def wende_element_effekt_an(winner, element, spieler_token, gegner_token, spieler_hand, gegner_hand, talon):
    # Vor dem Effekt wird der aktuelle Stand der Tokens angezeigt
    print(f"{FARBE_STAND}Vor dem Effekt: Spieler-Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")
    if element == "Feuer" und winner == "spieler":
        gegner_token -= 1  # Feuer verringert die Tokens des Gegners
    elif element == "Wasser" und winner == "spieler":
        spieler_token += 1  # Wasser erhöht die Tokens des Spielers
        gegner_token -= 1  # ...und verringert die Tokens des Gegners
    elif element == "Erde" und winner == "spieler":
        spieler_token += 1  # Erde erhöht die Tokens des Spielers
    elif element == "Luft" und winner == "spieler":
        spieler_token += 2  # Luft gibt dem Spieler 2 zusätzliche Tokens
        print(f"{FARBE_SPIELER}Du erhältst 2 zusätzliche Tokens!{FARBE_RESET}")
    elif element == "Feuer" und winner == "gegner":
        spieler_token -= 1  # Feuer verringert die Tokens des Spielers
    elif element == "Wasser" und winner == "gegner":
        gegner_token += 1  # Wasser erhöht die Tokens des Gegners
        spieler_token -= 1  # ...und verringert die Tokens des Spielers
    elif element == "Erde" und winner == "gegner":
        gegner_token += 1  # Erde erhöht die Tokens des Gegners
    elif element == "Luft" und winner == "gegner":
        gegner_token += 2  # Luft gibt dem Gegner 2 zusätzliche Tokens
        print(f"{FARBE_KI}Die KI erhält 2 zusätzliche Tokens!{FARBE_RESET}")
    # Nach dem Effekt wird der neue Stand der Tokens angezeigt
    print(f"{FARBE_STAND}Nach dem Effekt: Spieler-Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")
    return spieler_token, gegner_token  # Die aktualisierten Token-Werte werden zurückgegeben

# Funktion zur Auswahl der besten KI-Karte basierend auf den Vorhersagen des Modells
def ki_waehlt_karte(gegner_hand, spieler_karte, spieler_token, gegner_token):
    beste_karte = None
    beste_wahrscheinlichkeit = -1

    for gegner_karte in gegner_hand:
        # Kodierung der Karten in numerische Features für das Modell
        spieler_karte_code = label_encoder_karten.transform([f"{spieler_karte[0]} {spieler_karte[1]}"])[0]
        gegner_karte_code = label_encoder_karten.transform([f"{gegner_karte[0]} {gegner_karte[1]}"])[0]

        # Erstellen der Feature-Matrix für die Vorhersage
        features = np.array([[spieler_karte_code, gegner_karte_code, spieler_token, gegner_token]])

        # Vorhersage des Modells: Wahrscheinlichkeit, dass der Spieler gewinnt
        vorhersage = modell.predict(features)
        wahrscheinlichkeit = vorhersage[0][0]

        # Die Karte mit der besten (höchsten) Wahrscheinlichkeit wird ausgewählt
        if wahrscheinlichkeit > beste_wahrscheinlichkeit:
            beste_wahrscheinlichkeit = wahrscheinlichkeit
            beste_karte = gegner_karte

    return beste_karte  # Die ausgewählte Karte wird zurückgegeben

# Funktion, um ein Spiel gegen die KI zu spielen
def spiele_gegen_ki():
    # Ein neues Deck wird generiert und gemischt
    deck = deck_generieren()
    # Die ersten vier Karten gehen an den Spieler, die nächsten vier an die KI
    spieler_hand = deck[:4]
    gegner_hand = deck[4:8]
    # Der Rest bildet den Talon (Stapel der verbleibenden Karten)
    talon = deck[8:]

    # Beide Spieler starten mit 5 Tokens
    spieler_token = 5
    gegner_token = 5

    # Spiel läuft, solange beide Spieler Tokens und Karten haben
    while spieler_token > 0 and gegner_token > 0 and (spieler_hand or gegner_hand):
        # Spielstand anzeigen
        print(f"{FARBE_STAND}\nDeine Karten: {spieler_hand}{FARBE_RESET}")
        print(f"{FARBE_STAND}Deine Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")

        # Überprüfen, ob der Spieler noch Karten hat
        if not spieler_hand:
            print(f"{FARBE_STAND}Du hast keine Karten mehr.{FARBE_RESET}")
            break

        # Spieler wählt eine Karte
        while True:
            try:
                # Spieler wählt eine Karte anhand der Indexposition
                karten_auswahl = int(input(f"{FARBE_SPIELER}Wähle eine Karte (1-{len(spieler_hand)}): {FARBE_RESET}")) - 1
                if 0 <= karten_auswahl < len(spieler_hand):
                    # Gewählte Karte wird aus der Hand des Spielers entfernt
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

        # Anwenden der Effekte basierend auf dem Element der Karte
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

    # Spielende und Ausgabe des Ergebnisses
    if spieler_token > 0 and not gegner_hand:
        print(f"{FARBE_GEWINNER_SPIELER}\nGlückwunsch! Du hast gegen die KI gewonnen!{FARBE_RESET}")
    elif gegner_token > 0 and not spieler_hand:
        print(f"{FARBE_GEWINNER_KI}\nDie KI hat gewonnen. Versuch es noch einmal!{FARBE_RESET}")
    else:
        print(f"{FARBE_STAND}\nDas Spiel endet in einem Unentschieden.{FARBE_RESET}")

# Spiel starten, wenn das Skript direkt ausgeführt wird
if __name__ == "__main__":
    spiele_gegen_ki()
