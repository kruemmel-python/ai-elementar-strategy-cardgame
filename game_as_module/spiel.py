import os
import random
from konstanten import ELEMENTE, WERTE, ELEMENT_HIERARCHIE, HELDEN, label_encoder_karten, label_encoder_held, label_encoder_wetter, label_encoder_wert

class Spiel:
    def __init__(self):
        self.deck = self.deck_generieren()
        self.spieler_hand = self.deck[:4]
        self.gegner_hand = self.deck[4:8]
        self.talon = self.deck[8:]
        self.spieler_token = 5
        self.gegner_token = 5
        self.held = random.choice(list(HELDEN.keys()))
        self.gegner_held = random.choice(list(HELDEN.keys()))
        self.wettereffekt = None
        self.gewinner = None
        self.spieler_karte = None
        self.gegner_karte = None
        self.spieler_elementbonus = 0
        self.spieler_heldenbonus = 0
        self.spieler_bonus = 0
        self.gegner_elementbonus = 0
        self.gegner_heldenbonus = 0
        self.gegner_bonus = 0
        self.spieler_gesamtwert = 0
        self.gegner_gesamtwert = 0
        self.abgelegte_spieler_karten = []  # Liste für abgelegte Spielerkarten
        self.abgelegte_gegner_karten = [] # Liste für abgelegte Gegnerkarten

    def deck_generieren(self):
        """Generates a shuffled deck of cards."""
        deck = [(element, wert) for element in ELEMENTE for wert in WERTE]
        random.shuffle(deck)
        return deck

    def zufaelliges_wetter(self):
        """
        Randomly selects a weather event and prints it.

        Returns:
            dict: A dictionary representing the weather effects.
        """
        wetter = random.choice(["Regen", "Windsturm", "Erdbeben"])
        print(f"Wetterereignis: {wetter}")
        if wetter == "Regen":
            return {"Wasser": 1, "Feuer": -1}
        elif wetter == "Windsturm":
            return {"Luft": 2, "Erde": -1}
        return {}

    def berechne_gesamtwert(self, karte, gegner_karte, spieler_held, gegner_held):
        """Calculates the total value of a card."""
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

    def berechne_token_bonus(self, tokens):
        """Calculates token bonus."""
        if tokens <= 2:
            return 0
        elif tokens <= 5:
            return 2
        elif tokens <= 9:
            return 4
        else:
            return 6

    def bestimme_gewinner(self):
        """Determines the winner of the battle."""
        spieler_gesamtwert, self.spieler_elementbonus, self.spieler_heldenbonus = self.berechne_gesamtwert(self.spieler_karte, self.gegner_karte, HELDEN[self.held], HELDEN[self.gegner_held])
        self.spieler_bonus = self.berechne_token_bonus(self.spieler_token)
        self.spieler_gesamtwert = spieler_gesamtwert + self.spieler_bonus

        gegner_gesamtwert, self.gegner_elementbonus, self.gegner_heldenbonus = self.berechne_gesamtwert(self.gegner_karte, self.spieler_karte, HELDEN[self.gegner_held], HELDEN[self.held])
        self.gegner_bonus = self.berechne_token_bonus(self.gegner_token)
        self.gegner_gesamtwert = gegner_gesamtwert + self.gegner_bonus

        if self.spieler_gesamtwert > self.gegner_gesamtwert:
            self.gewinner = "spieler"
        elif self.gegner_gesamtwert > self.spieler_gesamtwert:
            self.gewinner = "gegner"
        else:
            self.gewinner = "unentschieden"

    def wende_element_effekt_an(self):
        """Applies element effects based on the winner."""
        if self.spieler_karte is None:
           return
        element = self.spieler_karte[0]
        if element == "Feuer" and self.gewinner == "spieler":
            self.gegner_token -= 1
        elif element == "Wasser" and self.gewinner == "spieler":
            self.spieler_token += 1
            self.gegner_token -= 1
        elif element == "Erde" and self.gewinner == "spieler":
            self.spieler_token += 1
        elif element == "Luft" and self.gewinner == "spieler":
            self.spieler_token += 2
        elif element == "Feuer" and self.gewinner == "gegner":
            self.spieler_token -= 1
        elif element == "Wasser" and self.gewinner == "gegner":
            self.gegner_token += 1
            self.spieler_token -= 1
        elif element == "Erde" and self.gewinner == "gegner":
            self.gegner_token += 1
        elif element == "Luft" and self.gewinner == "gegner":
            self.gegner_token += 2

    def ki_karte_waehlen(self):
        """AI chooses a card."""
        if self.gegner_hand:
            self.gegner_karte = random.choice(self.gegner_hand)
            self.abgelegte_gegner_karten.append(self.gegner_karte)
            self.gegner_hand.remove(self.gegner_karte)
        else:
            self.gegner_karte = None
            print("Die KI hat keine Karten mehr.")

    def karte_waehlen(self, karten_index):
        """Player chooses a card."""
        if 0 <= karten_index < len(self.spieler_hand):
            self.spieler_karte = self.spieler_hand.pop(karten_index)
            self.abgelegte_spieler_karten.append(self.spieler_karte)

            self.ki_karte_waehlen()
            self.bestimme_gewinner()
            self.wende_element_effekt_an()

            if self.talon:
                if len(self.spieler_hand) < 4:
                    self.spieler_hand.append(self.talon.pop())
                if len(self.gegner_hand) < 4:
                    self.gegner_hand.append(self.talon.pop())
            return True
        return False

    def spiel_ende(self):
        """Checks if the game has ended."""
        return self.spieler_token <= 0 or self.gegner_token <= 0 or not (self.spieler_hand or self.gegner_hand)

    def get_gewinner_text(self):
        """Get the winner text."""
        if self.spieler_token > self.gegner_token:
            return "Glückwunsch! Du hast gegen die KI gewonnen!"
        elif self.gegner_token > self.spieler_token:
            return "Die KI hat gewonnen. Versuch es noch einmal!"
        else:
            return "Das Spiel endet in einem Unentschieden."
