import os  # Importiert das 'os'-Modul, das Funktionen für Interaktionen mit dem Betriebssystem bereitstellt (hier nicht direkt verwendet, aber oft nützlich)
import random  # Importiert das 'random'-Modul, um Zufallszahlen zu generieren
from konstanten import ELEMENTE, WERTE, ELEMENT_HIERARCHIE, HELDEN, label_encoder_karten, label_encoder_held, label_encoder_wetter, label_encoder_wert  # Importiert Konstanten und Label-Encoder aus der Datei 'konstanten.py'

class Spiel:
    """
    Eine Klasse, die ein einfaches Kartenspiel gegen eine KI repräsentiert.

    Attribute:
        deck (list): Das gesamte Kartendeck.
        spieler_hand (list): Die Karten auf der Hand des Spielers.
        gegner_hand (list): Die Karten auf der Hand des Gegners (KI).
        talon (list): Die restlichen Karten, die noch nicht verteilt wurden.
        spieler_token (int): Die Token des Spielers (Lebenspunkte).
        gegner_token (int): Die Token des Gegners (Lebenspunkte).
        held (str): Der vom Spieler gewählte Held.
        gegner_held (str): Der vom Gegner (KI) gewählte Held.
        wettereffekt (dict oder None): Der aktuelle Wettereffekt (falls vorhanden).
        gewinner (str oder None): Der Gewinner der aktuellen Runde ("spieler", "gegner" oder "unentschieden").
        spieler_karte (tuple oder None): Die vom Spieler gespielte Karte.
        gegner_karte (tuple oder None): Die von der KI gespielte Karte.
        spieler_elementbonus (int): Der Elementbonus des Spielers.
        spieler_heldenbonus (int): Der Heldenbonus des Spielers.
        spieler_bonus (int): Der Gesamtbonus des Spielers (Element + Held + Token).
        gegner_elementbonus (int): Der Elementbonus des Gegners.
        gegner_heldenbonus (int): Der Heldenbonus des Gegners.
        gegner_bonus (int): Der Gesamtbonus des Gegners (Element + Held + Token).
        spieler_gesamtwert (int): Der Gesamtwert der Karte des Spielers.
        gegner_gesamtwert (int): Der Gesamtwert der Karte des Gegners.
        abgelegte_spieler_karten (list): Eine Liste der vom Spieler abgelegten Karten.
        abgelegte_gegner_karten (list): Eine Liste der vom Gegner abgelegten Karten.

    Methoden:
        __init__(): Initialisiert ein neues Spiel.
        deck_generieren(): Erstellt und mischt ein neues Kartendeck.
        zufaelliges_wetter(): Wählt zufällig ein Wetterereignis aus.
        berechne_gesamtwert(karte, gegner_karte, spieler_held, gegner_held): Berechnet den Gesamtwert einer Karte unter Berücksichtigung von Elementen und Helden.
        berechne_token_bonus(tokens): Berechnet den Bonus basierend auf der Anzahl der Token.
        bestimme_gewinner(): Bestimmt den Gewinner einer Runde.
        wende_element_effekt_an(): Wendet Elementeffekte basierend auf dem Gewinner an.
        ki_karte_waehlen(): Lässt die KI eine Karte aus ihrer Hand wählen.
        karte_waehlen(karten_index): Lässt den Spieler eine Karte aus seiner Hand wählen.
        spiel_ende(): Überprüft, ob das Spiel beendet ist.
        get_gewinner_text(): Gibt den Gewinnertext zurück.
    """
    def __init__(self):
        """
        Initialisiert ein neues Spiel.

        Die Methode erstellt ein neues Kartendeck, teilt Karten an Spieler und KI aus,
        setzt die Token-Anzahl auf 5, wählt zufällig Helden für Spieler und KI aus,
        initialisiert Wettereffekte und andere Attribute.
        """
        self.deck = self.deck_generieren()  # Erstellt ein gemischtes Deck
        self.spieler_hand = self.deck[:4]  # Die ersten 4 Karten für den Spieler
        self.gegner_hand = self.deck[4:8]  # Die nächsten 4 Karten für die KI
        self.talon = self.deck[8:]  # Die restlichen Karten bilden den Talon
        self.spieler_token = 5  # Start-Token für den Spieler
        self.gegner_token = 5  # Start-Token für den Gegner
        self.held = random.choice(list(HELDEN.keys()))  # Wählt zufällig einen Helden für den Spieler
        self.gegner_held = random.choice(list(HELDEN.keys()))  # Wählt zufällig einen Helden für die KI
        self.wettereffekt = None  # Initialisiert den Wettereffekt
        self.gewinner = None  # Initialisiert den Gewinner
        self.spieler_karte = None # Initialisiert die Spielerkarte
        self.gegner_karte = None # Initialisiert die Gegnerkarte
        self.spieler_elementbonus = 0 # Initialisiert den Elementbonus des Spielers
        self.spieler_heldenbonus = 0 # Initialisiert den Heldenbonus des Spielers
        self.spieler_bonus = 0 # Initialisiert den Gesamtbonus des Spielers
        self.gegner_elementbonus = 0 # Initialisiert den Elementbonus des Gegners
        self.gegner_heldenbonus = 0 # Initialisiert den Heldenbonus des Gegners
        self.gegner_bonus = 0 # Initialisiert den Gesamtbonus des Gegners
        self.spieler_gesamtwert = 0 # Initialisiert den Gesamtwert der Karte des Spielers
        self.gegner_gesamtwert = 0 # Initialisiert den Gesamtwert der Karte des Gegners
        self.abgelegte_spieler_karten = []  # Initialisiert eine Liste für abgelegte Spielerkarten
        self.abgelegte_gegner_karten = [] # Initialisiert eine Liste für abgelegte Gegnerkarten

    def deck_generieren(self):
        """Generates a shuffled deck of cards.
        Erzeugt ein gemischtes Kartendeck.

        Gibt:
            list: Eine Liste von Karten (Tupel von Element und Wert).
        """
        deck = [(element, wert) for element in ELEMENTE for wert in WERTE]  # Erstellt alle möglichen Kartenkombinationen
        random.shuffle(deck)  # Mischt das Deck zufällig
        return deck

    def zufaelliges_wetter(self):
        """
        Wählt zufällig ein Wetterereignis aus und gibt die entsprechenden Effekte zurück.
        
        Gibt:
           dict: Ein Dictionary mit Wettereffekten oder ein leeres Dictionary, falls kein Wettereffekt.
        """
        wetter = random.choice(["Regen", "Windsturm", "Erdbeben"]) # Wählt zufällig ein Wetterereignis aus
        print(f"Wetterereignis: {wetter}")  # Gibt das Wetterereignis aus
        if wetter == "Regen":  # Wenn es regnet
            return {"Wasser": 1, "Feuer": -1}  # Wasser-Element ist stärker, Feuer-Element ist schwächer
        elif wetter == "Windsturm":  # Wenn ein Windsturm ist
            return {"Luft": 2, "Erde": -1}  # Luft-Element ist stärker, Erde-Element ist schwächer
        return {} # Gibt ein leeres Dictionary zurück, wenn kein Wettereffekt zutrifft

    def berechne_gesamtwert(self, karte, gegner_karte, spieler_held, gegner_held):
        """Berechnet den Gesamtwert einer Karte.

        Der Gesamtwert setzt sich aus dem Wert der Karte, dem Elementbonus und dem Heldenbonus zusammen.

        Args:
            karte (tuple): Die Karte des Spielers (Element, Wert).
            gegner_karte (tuple): Die Karte des Gegners (Element, Wert).
            spieler_held (dict): Der Held des Spielers (mit Element und Bonus).
            gegner_held (dict): Der Held des Gegners (mit Element und Bonus).

        Gibt:
            tuple: Der Gesamtwert, der Elementbonus, der Heldenbonus.
        """
        element, wert = karte  # Entpackt die Karte des Spielers in Element und Wert
        gegner_element, gegner_wert = gegner_karte # Entpackt die Karte des Gegners in Element und Wert
        wert_index = WERTE.index(wert) # Findet den Index des Kartenwerts im WERTE Array

        # Berechnet den Elementbonus basierend auf der Elementhierarchie
        if gegner_element in ELEMENT_HIERARCHIE[element]:
            element_bonus = ELEMENT_HIERARCHIE[element][gegner_element]  # Gibt den Bonus basierend auf der Element-Hierarchie
        else:
            element_bonus = 0  # Kein Bonus, wenn die Elemente keine Beziehung zueinander haben

        # Berechnet den Heldenbonus, wenn das Element der Karte mit dem Element des Helden übereinstimmt
        helden_bonus = 0
        if spieler_held["Element"] == element:
            helden_bonus = spieler_held["Bonus"] # Gibt den Bonus des Helden

        gesamtwert = wert_index + element_bonus + helden_bonus # Berechnet den Gesamtwert der Karte
        return gesamtwert, element_bonus, helden_bonus # Gibt den Gesamtwert, Elementbonus und Heldenbonus zurück

    def berechne_token_bonus(self, tokens):
        """Berechnet den Bonus basierend auf der Anzahl der Token.

        Args:
            tokens (int): Die Anzahl der Token.

        Gibt:
            int: Der Token-Bonus.
        """
        if tokens <= 2:  # Wenn der Spieler 2 oder weniger Token hat
            return 0  # Kein Token-Bonus
        elif tokens <= 5:  # Wenn der Spieler 3 bis 5 Token hat
            return 2  # Kleiner Token-Bonus
        elif tokens <= 9:  # Wenn der Spieler 6 bis 9 Token hat
            return 4  # Mittlerer Token-Bonus
        else:  # Wenn der Spieler 10 oder mehr Token hat
            return 6  # Großer Token-Bonus

    def bestimme_gewinner(self):
        """Bestimmt den Gewinner der Runde.

        Die Methode berechnet den Gesamtwert für Spieler und KI und vergleicht diese.
        Zudem wird der Tokenbonus berechnet und hinzugefügt.
        """
        # Berechnet den Gesamtwert des Spielers, inklusive Element- und Heldenbonus
        spieler_gesamtwert, self.spieler_elementbonus, self.spieler_heldenbonus = self.berechne_gesamtwert(self.spieler_karte, self.gegner_karte, HELDEN[self.held], HELDEN[self.gegner_held])
        self.spieler_bonus = self.berechne_token_bonus(self.spieler_token) # Berechnet den Token-Bonus des Spielers
        self.spieler_gesamtwert = spieler_gesamtwert + self.spieler_bonus  # Fügt den Token-Bonus dem Gesamtwert des Spielers hinzu

        # Berechnet den Gesamtwert des Gegners, inklusive Element- und Heldenbonus
        gegner_gesamtwert, self.gegner_elementbonus, self.gegner_heldenbonus = self.berechne_gesamtwert(self.gegner_karte, self.spieler_karte, HELDEN[self.gegner_held], HELDEN[self.held])
        self.gegner_bonus = self.berechne_token_bonus(self.gegner_token) # Berechnet den Token-Bonus des Gegners
        self.gegner_gesamtwert = gegner_gesamtwert + self.gegner_bonus  # Fügt den Token-Bonus dem Gesamtwert des Gegners hinzu

        # Bestimmt den Gewinner basierend auf den Gesamtwerten
        if self.spieler_gesamtwert > self.gegner_gesamtwert:  # Wenn der Spieler einen höheren Gesamtwert hat
            self.gewinner = "spieler"  # Spieler gewinnt
        elif self.gegner_gesamtwert > self.spieler_gesamtwert:  # Wenn der Gegner einen höheren Gesamtwert hat
            self.gewinner = "gegner"  # Gegner gewinnt
        else:  # Wenn beide den gleichen Gesamtwert haben
            self.gewinner = "unentschieden"  # Unentschieden

    def wende_element_effekt_an(self):
        """Wendet Elementeffekte basierend auf dem Gewinner an.

        Abhängig vom Element der Karte des Spielers und dem Gewinner der Runde
        werden Token des Spielers oder des Gegners angepasst.
        """
        if self.spieler_karte is None:  # Überprüft, ob der Spieler überhaupt eine Karte gespielt hat
           return  # Wenn nicht, wird die Funktion abgebrochen.
        element = self.spieler_karte[0]  # Holt das Element der gespielten Karte des Spielers

        if element == "Feuer" and self.gewinner == "spieler": # Wenn der Spieler mit Feuer gewinnt
            self.gegner_token -= 1  # Verliert der Gegner 1 Token
        elif element == "Wasser" and self.gewinner == "spieler": # Wenn der Spieler mit Wasser gewinnt
            self.spieler_token += 1  # Gewinnt der Spieler 1 Token
            self.gegner_token -= 1  # Verliert der Gegner 1 Token
        elif element == "Erde" and self.gewinner == "spieler":  # Wenn der Spieler mit Erde gewinnt
            self.spieler_token += 1  # Gewinnt der Spieler 1 Token
        elif element == "Luft" and self.gewinner == "spieler": # Wenn der Spieler mit Luft gewinnt
            self.spieler_token += 2  # Gewinnt der Spieler 2 Token
        elif element == "Feuer" and self.gewinner == "gegner": # Wenn der Gegner mit Feuer gewinnt
            self.spieler_token -= 1  # Verliert der Spieler 1 Token
        elif element == "Wasser" and self.gewinner == "gegner": # Wenn der Gegner mit Wasser gewinnt
            self.gegner_token += 1 # Gewinnt der Gegner 1 Token
            self.spieler_token -= 1 # Verliert der Spieler 1 Token
        elif element == "Erde" and self.gewinner == "gegner": # Wenn der Gegner mit Erde gewinnt
            self.gegner_token += 1  # Gewinnt der Gegner 1 Token
        elif element == "Luft" and self.gewinner == "gegner": # Wenn der Gegner mit Luft gewinnt
            self.gegner_token += 2  # Gewinnt der Gegner 2 Token

    def ki_karte_waehlen(self):
        """Die KI wählt eine zufällige Karte aus ihrer Hand.
        """
        if self.gegner_hand: # Überprüft, ob die KI Karten auf der Hand hat
            self.gegner_karte = random.choice(self.gegner_hand)  # Wählt eine zufällige Karte aus der Hand der KI
            self.abgelegte_gegner_karten.append(self.gegner_karte)  # Fügt die gewählte Karte zu den abgelegten Karten der KI hinzu
            self.gegner_hand.remove(self.gegner_karte)  # Entfernt die Karte aus der Hand der KI
        else:  # Wenn die KI keine Karten mehr hat
            self.gegner_karte = None  # Setzt die Karte der KI auf None
            print("Die KI hat keine Karten mehr.") # Gibt eine Nachricht aus

    def karte_waehlen(self, karten_index):
        """Der Spieler wählt eine Karte aus seiner Hand.

        Args:
            karten_index (int): Der Index der gewählten Karte in der Hand des Spielers.

        Gibt:
            bool: True, wenn eine Karte erfolgreich gewählt wurde, sonst False.
        """
        if 0 <= karten_index < len(self.spieler_hand): # Überprüft, ob der Index gültig ist
            self.spieler_karte = self.spieler_hand.pop(karten_index)  # Entfernt die Karte vom Index aus der Hand des Spielers
            self.abgelegte_spieler_karten.append(self.spieler_karte) # Fügt die gewählte Karte zu den abgelegten Karten des Spielers hinzu

            self.ki_karte_waehlen()  # Lässt die KI eine Karte wählen
            self.bestimme_gewinner()  # Bestimmt den Gewinner der Runde
            self.wende_element_effekt_an()  # Wendet Elementeffekte an

            # Überprüft, ob der Talon noch Karten hat
            if self.talon:
                # Wenn der Spieler weniger als 4 Karten hat, wird eine vom Talon gezogen
                if len(self.spieler_hand) < 4:
                    self.spieler_hand.append(self.talon.pop())
                # Wenn der Gegner weniger als 4 Karten hat, wird eine vom Talon gezogen
                if len(self.gegner_hand) < 4:
                    self.gegner_hand.append(self.talon.pop())
            return True # Gibt True zurück, wenn erfolgreich
        return False # Gibt False zurück, wenn kein gültiger Index eingegeben wurde

    def spiel_ende(self):
        """Überprüft, ob das Spiel beendet ist.

        Das Spiel ist beendet, wenn ein Spieler keine Token mehr hat oder beide keine Karten mehr haben.

        Gibt:
            bool: True, wenn das Spiel beendet ist, sonst False.
        """
        # Gibt True zurück, wenn das Spielende erreicht wurde (wenn die Token eines Spielers 0 oder weniger betragen oder wenn beide Spieler keine Karten mehr haben)
        return self.spieler_token <= 0 or self.gegner_token <= 0 or not (self.spieler_hand or self.gegner_hand)

    def get_gewinner_text(self):
        """Gibt den Gewinnertext aus.
        
        Gibt:
            str: Der Gewinnertext.
        """
        if self.spieler_token > self.gegner_token: # Wenn der Spieler mehr Token hat
            return "Glückwunsch! Du hast gegen die KI gewonnen!"  # Gibt eine Gewinnnachricht aus
        elif self.gegner_token > self.spieler_token:  # Wenn der Gegner mehr Token hat
            return "Die KI hat gewonnen. Versuch es noch einmal!"  # Gibt eine Verlustnachricht aus
        else:
            return "Das Spiel endet in einem Unentschieden." # Gibt eine Unentschieden Nachricht aus
