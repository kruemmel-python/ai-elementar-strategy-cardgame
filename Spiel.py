import os
import time  # Für Zeitverzögerung
import random
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np

ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft", "Blitz", "Eis", "Magie"]
WERTE = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]

ELEMENT_HIERARCHIE = {
    "Wasser": {"Feuer": 3, "Erde": 1, "Luft": -3, "Blitz": -3, "Eis": 3},
    "Feuer": {"Erde": 3, "Luft": 1, "Wasser": -3, "Eis": 1, "Blitz": 1},
    "Erde": {"Luft": 3, "Wasser": -1, "Feuer": -3, "Blitz": 3, "Eis": 1},
    "Luft": {"Wasser": 3, "Erde": -1, "Feuer": -3, "Eis": 3, "Blitz": -1},
    "Blitz": {"Wasser": 3, "Erde": 1, "Feuer": 1, "Luft": -3, "Eis": -1},
    "Eis": {"Feuer": 3, "Erde": 1, "Wasser": -3, "Luft": 1, "Blitz": 3},
    "Magie": {"Feuer": 1, "Wasser": 1, "Erde": 1, "Luft": 1, "Blitz": 2, "Eis": 2}
}

HELDEN = {
    "Drache": {"Element": "Feuer", "Bonus": 2},  # Drache hat Bonus auf Feuer
    "Zauberer": {"Element": "Magie", "Bonus": 3}  # Zauberer hat Bonus auf Magie
}

FARBE_SPIELER = "\033[96m"
FARBE_KI = "\033[93m"
FARBE_GEWINNER_SPIELER = "\033[92m"
FARBE_GEWINNER_KI = "\033[91m"
FARBE_STAND = "\033[97m"
FARBE_RESET = "\033[0m"

# Ensure the LabelEncoder for cards includes the elements correctly
label_encoder_karten = LabelEncoder()
label_encoder_karten.fit(ELEMENTE)

# Hero encoding (important)
label_encoder_held = LabelEncoder()
label_encoder_held.fit(list(HELDEN.keys()))

# One-Hot-Encoder for heroes
one_hot_encoder_held = OneHotEncoder(sparse_output=False)
one_hot_encoder_held.fit(np.array(list(HELDEN.keys())).reshape(-1, 1))

# Weather encoding
label_encoder_wetter = LabelEncoder()
label_encoder_wetter.fit(["Regen", "Windsturm", "Erdbeben"])

# Card value encoding
label_encoder_wert = LabelEncoder()
label_encoder_wert.fit(WERTE)

# Load model
modell_pfad = "Simulationen/elementar_schlacht_modell.keras"
modell = load_model(modell_pfad)

def deck_generieren():
    """
    Generates a shuffled deck of cards consisting of elements and values.

    Returns:
        list: A list of tuples representing the shuffled deck of cards.
    """
    deck = [(element, wert) for element in ELEMENTE for wert in WERTE]
    random.shuffle(deck)
    return deck

def zufaelliges_wetter():
    """
    Randomly selects a weather event and prints it.

    Returns:
        dict: A dictionary representing the weather effects.
    """
    wetter = random.choice(["Regen", "Windsturm", "Erdbeben"])
    print(f"{FARBE_STAND}Wetterereignis: {wetter}{FARBE_RESET}")
    if wetter == "Regen":
        return {"Wasser": 1, "Feuer": -1}
    elif wetter == "Windsturm":
        return {"Luft": 2, "Erde": -1}
    return {}

def drehe_symbol(sekunden):
    """
    Displays a spinning symbol animation for a specified number of seconds.

    Args:
        sekunden (int): The number of seconds to display the animation.
    """
    animation = ['\\', '|', '/', '-']
    for i in range(sekunden * 10):
        print(f"\r{animation[i % len(animation)]} ", end="")
        time.sleep(0.1)
    print("\r", end="")

def berechne_gesamtwert(karte, gegner_karte, spieler_held, gegner_held):
    """
    Calculates the total value of a card considering element and hero bonuses.

    Args:
        karte (tuple): The player's card.
        gegner_karte (tuple): The opponent's card.
        spieler_held (dict): The player's hero.
        gegner_held (dict): The opponent's hero.

    Returns:
        tuple: The total value, element bonus, and hero bonus.
    """
    element, wert = karte
    gegner_element, gegner_wert = gegner_karte
    wert_index = WERTE.index(wert)

    # Calculate element bonus
    if gegner_element in ELEMENT_HIERARCHIE[element]:
        element_bonus = ELEMENT_HIERARCHIE[element][gegner_element]
    else:
        element_bonus = 0

    # Consider hero bonus only if the played element matches the hero's element
    helden_bonus = 0
    if spieler_held["Element"] == element:
        helden_bonus = spieler_held["Bonus"]

    gesamtwert = wert_index + element_bonus + helden_bonus
    return gesamtwert, element_bonus, helden_bonus

def berechne_token_bonus(tokens):
    """
    Calculates the token bonus based on the number of tokens.

    Args:
        tokens (int): The number of tokens.

    Returns:
        int: The token bonus.
    """
    if tokens <= 2:
        return 0
    elif tokens <= 5:
        return 2
    elif tokens <= 9:
        return 4
    else:
        return 6

def zeige_auswertung(spieler_karte, gegner_karte, spieler_token, gegner_token, spieler_gesamtwert, gegner_gesamtwert, spieler_bonus, gegner_bonus, spieler_elementbonus, gegner_elementbonus, spieler_heldenbonus, gegner_heldenbonus):
    """
    Displays the evaluation of the cards played by the player and the AI.

    Args:
        spieler_karte (tuple): The player's card.
        gegner_karte (tuple): The AI's card.
        spieler_token (int): The player's tokens.
        gegner_token (int): The AI's tokens.
        spieler_gesamtwert (int): The player's total value.
        gegner_gesamtwert (int): The AI's total value.
        spieler_bonus (int): The player's token bonus.
        gegner_bonus (int): The AI's token bonus.
        spieler_elementbonus (int): The player's element bonus.
        gegner_elementbonus (int): The AI's element bonus.
        spieler_heldenbonus (int): The player's hero bonus.
        gegner_heldenbonus (int): The AI's hero bonus.
    """
    print("\n**********************************************************************************************************************************************")
    print("Auswertung:")
    print(f"Spieler spielt: {spieler_karte[0]} {spieler_karte[1]}")
    print(f"Spieler Kartenwert = {WERTE.index(spieler_karte[1])} (Index von {spieler_karte[1]} in der Liste WERTE)")
    print(f"Spieler Elementbonus = {spieler_elementbonus}")
    print(f"Spieler Heldenbonus = {spieler_heldenbonus}")
    print(f"Spieler hat {spieler_token} Tokens → Tokenbonus = {spieler_bonus}")
    print(f"Gesamtwert Spieler = {WERTE.index(spieler_karte[1])} (Kartenwert) + {spieler_elementbonus} (Elementbonus) + {spieler_heldenbonus} (Heldenbonus) + {spieler_bonus} (Tokenbonus) = {spieler_gesamtwert}")

    print(f"\nKI spielt: {gegner_karte[0]} {gegner_karte[1]}")
    print(f"KI Kartenwert = {WERTE.index(gegner_karte[1])} (Index von {gegner_karte[1]} in der Liste WERTE)")
    print(f"KI Elementbonus = {gegner_elementbonus}")
    print(f"KI Heldenbonus = {gegner_heldenbonus}")
    print(f"KI hat {gegner_token} Tokens → Tokenbonus = {gegner_bonus}")
    print(f"Gesamtwert KI = {WERTE.index(gegner_karte[1])} (Kartenwert) + {gegner_elementbonus} (Elementbonus) + {gegner_heldenbonus} (Heldenbonus) + {gegner_bonus} (Tokenbonus) = {gegner_gesamtwert}")
    print("************************************************************************************************************************************************\n")

def bestimme_gewinner(spieler_karte, gegner_karte, spieler_token, gegner_token, spieler_held, gegner_held):
    """
    Determines the winner of a battle based on card values and bonuses.

    Args:
        spieler_karte (tuple): The player's card.
        gegner_karte (tuple): The AI's card.
        spieler_token (int): The player's tokens.
        gegner_token (int): The AI's tokens.
        spieler_held (str): The player's hero.
        gegner_held (str): The AI's hero.

    Returns:
        str: The winner of the battle ("spieler", "gegner", or "unentschieden").
    """
    spieler_gesamtwert, spieler_elementbonus, spieler_heldenbonus = berechne_gesamtwert(spieler_karte, gegner_karte, HELDEN[spieler_held], HELDEN[gegner_held])
    spieler_bonus = berechne_token_bonus(spieler_token)
    spieler_gesamtwert += spieler_bonus

    gegner_gesamtwert, gegner_elementbonus, gegner_heldenbonus = berechne_gesamtwert(gegner_karte, spieler_karte, HELDEN[gegner_held], HELDEN[spieler_held])
    gegner_bonus = berechne_token_bonus(gegner_token)
    gegner_gesamtwert += gegner_bonus

    print("Spiel wird analysiert, bitte warten....")
    drehe_symbol(3)

    zeige_auswertung(spieler_karte, gegner_karte, spieler_token, gegner_token, spieler_gesamtwert, gegner_gesamtwert, spieler_bonus, gegner_bonus, spieler_elementbonus, gegner_elementbonus, spieler_heldenbonus, gegner_heldenbonus)

    if spieler_gesamtwert > gegner_gesamtwert:
        return "spieler"
    elif gegner_gesamtwert > spieler_gesamtwert:
        return "gegner"
    else:
        return "unentschieden"

def wende_element_effekt_an(winner, element, spieler_token, gegner_token):
    """
    Applies element effects based on the winner.

    Args:
        winner (str): The winner of the battle ("spieler" or "gegner").
        element (str): The element of the card.
        spieler_token (int): The player's elemental points.
        gegner_token (int): The opponent's elemental points.

    Returns:
        tuple: The updated elemental points for the player and the opponent.
    """
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

def spiele_gegen_ki():
    """
    Simulates a game against the AI.
    """
    deck = deck_generieren()
    spieler_hand = deck[:4]
    gegner_hand = deck[4:8]
    talon = deck[8:]
    spieler_token = 5
    gegner_token = 5
    held = random.choice(list(HELDEN.keys()))  # Spieler bekommt zufälligen Helden
    gegner_held = random.choice(list(HELDEN.keys()))  # KI bekommt zufälligen Helden
    print(f"{FARBE_SPIELER}Du spielst mit dem Helden: {held} ({HELDEN[held]['Bonus']} Bonus auf {HELDEN[held]['Element']})! {FARBE_RESET}")

    while spieler_token > 0 and gegner_token > 0 and (spieler_hand or gegner_hand):
        print(f"{FARBE_STAND}\nDeine Karten: {spieler_hand}{FARBE_RESET}")
        print(f"{FARBE_STAND}Deine Tokens: {spieler_token}, KI-Tokens: {gegner_token}{FARBE_RESET}")

        wettereffekt = zufaelliges_wetter()

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
        if gegner_hand:
            gegner_karte = random.choice(gegner_hand)
            gegner_hand.remove(gegner_karte)
        else:
            print(f"{FARBE_KI}Die KI hat keine Karten mehr.{FARBE_RESET}")
            break

        print(f"{FARBE_SPIELER}Du spielst: {spieler_karte}{FARBE_RESET}")
        print(f"{FARBE_KI}Die KI spielt: {gegner_karte}{FARBE_RESET}")

        winner = bestimme_gewinner(spieler_karte, gegner_karte, spieler_token, gegner_token, held, gegner_held)
        if winner == "spieler":
            print(f"{FARBE_GEWINNER_SPIELER}Der Gewinner des Schlages ist: {winner}{FARBE_RESET}")
        elif winner == "gegner":
            print(f"{FARBE_GEWINNER_KI}Der Gewinner des Schlages ist: {winner}{FARBE_RESET}")
        else:
            print(f"{FARBE_STAND}Der Schlag endet unentschieden.{FARBE_RESET}")

        spieler_token, gegner_token = wende_element_effekt_an(winner, spieler_karte[0], spieler_token, gegner_token)

        if talon:
            if len(spieler_hand) < 4:
                spieler_hand.append(talon.pop())
            if len(gegner_hand) < 4:
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
