import os
import time  # Für Zeitverzögerung
import random
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder
import numpy as np

ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft"]
WERTE = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]

ELEMENT_HIERARCHIE = {
    "Wasser": {"Feuer": 3, "Erde": 1, "Luft": -3},
    "Feuer": {"Erde": 3, "Luft": 1, "Wasser": -3},
    "Erde": {"Luft": 3, "Wasser": 1, "Feuer": -3},
    "Luft": {"Wasser": 3, "Feuer": 1, "Erde": -3}
}

FARBE_SPIELER = "\033[96m"
FARBE_KI = "\033[93m"
FARBE_GEWINNER_SPIELER = "\033[92m"
FARBE_GEWINNER_KI = "\033[91m"
FARBE_STAND = "\033[97m"
FARBE_RESET = "\033[0m"

# Kartenkodierung
label_encoder_karten = LabelEncoder()
label_encoder_karten.fit([f"{element} {wert}" for element in ELEMENTE for wert in WERTE])

# Modell laden
modell_pfad = "Simulationen/elementar_schlacht_modell.keras"
modell = load_model(modell_pfad)

def deck_generieren():
    deck = [(element, wert) for element in ELEMENTE for wert in WERTE]
    random.shuffle(deck)
    return deck

def berechne_gesamtwert(karte, gegner_karte):
    element, wert = karte
    gegner_element, gegner_wert = gegner_karte
    wert_index = WERTE.index(wert)

    if gegner_element in ELEMENT_HIERARCHIE[element]:
        element_bonus = ELEMENT_HIERARCHIE[element][gegner_element]
    else:
        element_bonus = 0

    gesamtwert = wert_index + element_bonus
    return gesamtwert, element_bonus

def berechne_token_bonus(tokens):
    if tokens <= 2:
        return 0
    elif tokens <= 5:
        return 2
    elif tokens <= 9:
        return 4
    else:
        return 6

def drehe_symbol(sekunden):
    animation = ['\\', '|', '/', '-']
    for i in range(sekunden * 10):
        print(f"\r{animation[i % len(animation)]} ", end="")
        time.sleep(0.1)
    print("\r", end="")  # Symbol entfernen

def zeige_auswertung(spieler_karte, gegner_karte, spieler_token, gegner_token, spieler_gesamtwert, gegner_gesamtwert, spieler_bonus, gegner_bonus, spieler_elementbonus, gegner_elementbonus):
    print("\n**********************************************************************************************************************************************")
    print("Auswertung:")
    print(f"Spieler spielt: {spieler_karte[0]} {spieler_karte[1]}")
    print(f"Spieler Kartenwert = {WERTE.index(spieler_karte[1])} (Index von {spieler_karte[1]} in der Liste WERTE)")
    print(f"Spieler Elementbonus = {spieler_elementbonus}")
    print(f"Spieler hat {spieler_token} Tokens → Tokenbonus = {spieler_bonus}")
    print(f"Gesamtwert Spieler = {WERTE.index(spieler_karte[1])} (Kartenwert) + {spieler_elementbonus} (Elementbonus) + {spieler_bonus} (Tokenbonus) = {spieler_gesamtwert}")

    print(f"\nKI spielt: {gegner_karte[0]} {gegner_karte[1]}")
    print(f"KI Kartenwert = {WERTE.index(gegner_karte[1])} (Index von {gegner_karte[1]} in der Liste WERTE)")
    print(f"KI Elementbonus = {gegner_elementbonus}")
    print(f"KI hat {gegner_token} Tokens → Tokenbonus = {gegner_bonus}")
    print(f"Gesamtwert KI = {WERTE.index(gegner_karte[1])} (Kartenwert) + {gegner_elementbonus} (Elementbonus) + {gegner_bonus} (Tokenbonus) = {gegner_gesamtwert}")
    print("************************************************************************************************************************************************\n")

def bestimme_gewinner(spieler_karte, gegner_karte, spieler_token, gegner_token):
    spieler_gesamtwert, spieler_elementbonus = berechne_gesamtwert(spieler_karte, gegner_karte)
    spieler_bonus = berechne_token_bonus(spieler_token)
    spieler_gesamtwert += spieler_bonus

    gegner_gesamtwert, gegner_elementbonus = berechne_gesamtwert(gegner_karte, spieler_karte)
    gegner_bonus = berechne_token_bonus(gegner_token)
    gegner_gesamtwert += gegner_bonus

    print("Spiel wird analysiert, bitte warten....")
    drehe_symbol(3)

    zeige_auswertung(spieler_karte, gegner_karte, spieler_token, gegner_token, spieler_gesamtwert, gegner_gesamtwert, spieler_bonus, gegner_bonus, spieler_elementbonus, gegner_elementbonus)

    if spieler_gesamtwert > gegner_gesamtwert:
        return "spieler"
    elif gegner_gesamtwert > spieler_gesamtwert:
        return "gegner"
    else:
        return "unentschieden"

def wende_element_effekt_an(winner, element, spieler_token, gegner_token):
    print(f"{FARBE_STAND}Vor dem Effekt: Spieler-Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")
    if element == "Feuer" and winner == "spieler":
        gegner_token -= 1
    elif element == "Wasser" and winner == "spieler":
        spieler_token += 1
        gegner_token -= 1
    elif element == "Erde" and winner == "spieler":
        spieler_token += 1
    elif element == "Luft" and winner == "spieler":
        spieler_token += 2
    elif element == "Feuer" and winner == "gegner":
        spieler_token -= 1
    elif element == "Wasser" and winner == "gegner":
        gegner_token += 1
        spieler_token -= 1
    elif element == "Erde" and winner == "gegner":
        gegner_token += 1
    elif element == "Luft" and winner == "gegner":
        gegner_token += 2
    print(f"{FARBE_STAND}Nach dem Effekt: Spieler-Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")
    return spieler_token, gegner_token

def ki_waehlt_karte(gegner_hand, spieler_karte, spieler_token, gegner_token):
    beste_karte = None
    beste_wahrscheinlichkeit = -1

    for gegner_karte in gegner_hand:
        spieler_karte_code = label_encoder_karten.transform([f"{spieler_karte[0]} {spieler_karte[1]}"])[0]
        gegner_karte_code = label_encoder_karten.transform([f"{gegner_karte[0]} {gegner_karte[1]}"])[0]

        features = np.array([[spieler_karte_code, gegner_karte_code, spieler_token, gegner_token]])
        vorhersage = modell.predict(features)
        wahrscheinlichkeit = vorhersage[0][0]

        if wahrscheinlichkeit > beste_wahrscheinlichkeit and wahrscheinlichkeit > 0.5:
            beste_wahrscheinlichkeit = wahrscheinlichkeit
            beste_karte = gegner_karte

    if beste_karte is None:
        beste_karte = random.choice(gegner_hand)

    print("\nKI überlegt...")
    drehe_symbol(3)

    print(f"{FARBE_KI}KI spielt: {beste_karte} mit einer Wahrscheinlichkeit von {beste_wahrscheinlichkeit:.2f} zu gewinnen.{FARBE_RESET}")
    return beste_karte

def spiele_gegen_ki():
    deck = deck_generieren()
    spieler_hand = deck[:4]
    gegner_hand = deck[4:8]
    talon = deck[8:]
    spieler_token = 5
    gegner_token = 5

    while spieler_token > 0 and gegner_token > 0 and (spieler_hand or gegner_hand):
        print(f"{FARBE_STAND}\nDeine Karten: {spieler_hand}{FARBE_RESET}")
        print(f"{FARBE_STAND}Deine Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")

        if not spieler_hand:
            print(f"{FARBE_STAND}Du hast keine Karten mehr.{FARBE_RESET}")
            break

        while True:
            try:
                karten_auswahl = int(input(f"{FARBE_SPIELER}Wähle eine Karte (1-{len(spieler_hand)}): {FARBE_RESET}")) - 1
                if 0 <= karten_auswahl < len(spieler_hand):
                    spieler_karte = spieler_hand.pop(karten_auswahl)
                    break
                else:
                    print(f"{FARBE_SPIELER}Ungültige Auswahl.{FARBE_RESET}")
            except ValueError:
                print(f"{FARFE_SPIELER}Ungültige Eingabe. Bitte eine Zahl eingeben.{FARBE_RESET}")

        if gegner_hand:
            gegner_karte = ki_waehlt_karte(gegner_hand, spieler_karte, spieler_token, gegner_token)
            gegner_hand.remove(gegner_karte)
        else:
            print(f"{FARBE_KI}Die KI hat keine Karten mehr.{FARBE_RESET}")
            break

        winner = bestimme_gewinner(spieler_karte, gegner_karte, spieler_token, gegner_token)
        if winner == "spieler":
            print(f"{FARBE_GEWINNER_SPIELER}Der Gewinner des Schlages ist: {winner}{FARBE_RESET}")
        elif winner == "gegner":
            print(f"{FARBE_GEWINNER_KI}Der Gewinner des Schlages ist: {winner}{FARBE_RESET}")
        else:
            print(f"{FARBE_STAND}Der Schlag endet unentschieden.{FARBE_RESET}")

        spieler_token, gegner_token = wende_element_effekt_an(
            winner, spieler_karte[0], spieler_token, gegner_token
        )

        if talon:
            if len(spieler_hand) < 4 and talon:
                spieler_hand.append(talon.pop())
            if len(gegner_hand) < 4 and talon:
                gegner_hand.append(talon.pop())

        print(f"{FARBE_STAND}\nDeine aktualisierten Karten: {spieler_hand}{FARBE_RESET}")

    if spieler_token > gegner_token:
        print(f"{FARBE_GEWINNER_SPIELER}\nGlückwunsch! Du hast gegen die KI gewonnen!{FARBE_RESET}")
    elif gegner_token > spieler_token:
        print(f"{FARBE_GEWINNER_KI}\nDie KI hat gewonnen. Versuch es noch einmal!{FARBE_RESET}")
    else:
        print(f"{FARBE_STAND}\nDas Spiel endet in einem Unentschieden.{FARBE_RESET}")

if __name__ == "__main__":
    spiele_gegen_ki()
