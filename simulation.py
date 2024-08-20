import csv  # Importiert das Modul zum Arbeiten mit CSV-Dateien.
import random  # Importiert das Modul zur Generierung von Zufallszahlen und zufälligen Auswahlmöglichkeiten.

# Definition der Karten und Elemente
ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft"]  # Definiert die vier Elemente im Spiel.
WERTE = ["7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]  # Definiert die möglichen Werte der Karten.
ANZAHL_ELEMENTAR_PUNKTE = 5  # Die Anzahl der Elementar-Punkte, mit denen jeder Spieler startet.

def deck_generieren():
    """
    Generiert ein gemischtes Kartendeck.

    Returns:
        list: Ein gemischtes Deck von Karten, wobei jede Karte eine Kombination aus Element und Wert ist.
    """
    deck = [(element, wert) for element in ELEMENTE for wert in WERTE]  # Erstellt das Deck durch Kombination der Elemente und Werte.
    random.shuffle(deck)  # Mischt das Deck, um die Reihenfolge der Karten zufällig zu machen.
    return deck  # Gibt das gemischte Deck zurück.

def spielstand_als_feature(spieler_hand, gegner_hand, spieler_token, gegner_token):
    """
    Erstellt eine Darstellung der aktuellen Spielsituation.

    Args:
        spieler_hand (list): Die Karten in der Hand des Spielers.
        gegner_hand (list): Die Karten in der Hand des Gegners.
        spieler_token (int): Die Anzahl der Tokens des Spielers.
        gegner_token (int): Die Anzahl der Tokens des Gegners.

    Returns:
        dict: Ein Dictionary, das die aktuelle Spielsituation beschreibt.
    """
    return {
        "spieler_hand": [str(karte) for karte in spieler_hand],  # Konvertiert die Karten des Spielers in Strings.
        "gegner_hand": [str(karte) for karte in gegner_hand],  # Konvertiert die Karten des Gegners in Strings.
        "spieler_token": spieler_token,  # Speichert die aktuelle Anzahl der Tokens des Spielers.
        "gegner_token": gegner_token  # Speichert die aktuelle Anzahl der Tokens des Gegners.
    }

def bestimme_gewinner(spieler_karte, gegner_karte):
    """
    Bestimmt den Gewinner eines Schlages basierend auf den Werten der Karten.

    Args:
        spieler_karte (tuple): Die Karte des Spielers als (Element, Wert).
        gegner_karte (tuple): Die Karte des Gegners als (Element, Wert).

    Returns:
        str: Der Gewinner des Schlages ("spieler", "gegner" oder "unentschieden").
    """
    spieler_wert_index = WERTE.index(spieler_karte[1])
    gegner_wert_index = WERTE.index(gegner_karte[1])

    if spieler_wert_index > gegner_wert_index:
        return "spieler"  # Der Spieler gewinnt, wenn seine Karte höher ist.
    elif gegner_wert_index > spieler_wert_index:
        return "gegner"  # Der Gegner gewinnt, wenn seine Karte höher ist.
    else:
        return "unentschieden"  # Es ist ein Unentschieden, wenn beide Karten gleich hoch sind.

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
    """
    Simuliert ein Spiel und sammelt die Spiel-Daten.

    Returns:
        list: Eine Liste von Dictionaries, die den Verlauf des Spiels beschreiben.
    """
    deck = deck_generieren()
    spieler_hand = deck[:4]
    gegner_hand = deck[4:8]
    talon = deck[8:]

    spieler_token = ANZAHL_ELEMENTAR_PUNKTE
    gegner_token = ANZAHL_ELEMENTAR_PUNKTE

    spiel_daten = []

    while spieler_token > 0 and gegner_token > 0:
        if spieler_hand:  # Überprüft, ob der Spieler Karten hat.
            spieler_karte = random.choice(spieler_hand)
            spieler_hand.remove(spieler_karte)
        else:
            break

        if gegner_hand:  # Überprüft, ob der Gegner Karten hat.
            gegner_karte = random.choice(gegner_hand)
            gegner_hand.remove(gegner_karte)
        else:
            break

        winner = bestimme_gewinner(spieler_karte, gegner_karte)
        spieler_token, gegner_token = wende_element_effekt_an(winner, spieler_karte[0], spieler_token, gegner_token)

        spielstand = spielstand_als_feature(spieler_hand, gegner_hand, spieler_token, gegner_token)
        spiel_daten.append({
            "spieler_karte": f"{spieler_karte[0]} {spieler_karte[1]}",
            "gegner_karte": f"{gegner_karte[0]} {gegner_karte[1]}",
            "spieler_token": spieler_token,
            "gegner_token": gegner_token,
            "gewinner": winner
        })

        if talon:
            if len(spieler_hand) < 4:
                spieler_hand.append(talon.pop())
            if len(gegner_hand) < 4:
                gegner_hand.append(talon.pop())

    return spiel_daten  # Gibt die gesammelten Spiel-Daten zurück.

def speichere_spieldaten_in_csv(spiel_daten, dateiname="Simulationen/spieldaten.csv"):
    """
    Speichert die Spieldaten in einer CSV-Datei.

    Args:
        spiel_daten (list): Eine Liste von Dictionaries, die den Spielverlauf beschreiben.
        dateiname (str): Der Name der CSV-Datei, in der die Daten gespeichert werden.
    """
    schluessel = spiel_daten[0].keys()
    with open(dateiname, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=schluessel)
        writer.writeheader()
        writer.writerows(spiel_daten)

def generiere_und_speichere_spiele(anzahl_spiele=10000):
    """
    Simuliert und speichert eine angegebene Anzahl von Spielen.

    Args:
        anzahl_spiele (int): Die Anzahl der zu simulierenden Spiele.
    """
    alle_spiel_daten = []
    for _ in range(anzahl_spiele):
        spiel_daten = simuliere_spiel()
        alle_spiel_daten.extend(spiel_daten)
    speichere_spieldaten_in_csv(alle_spiel_daten)

# Beispielaufruf zur Generierung und Speicherung von 10.000 Spielen
generiere_und_speichere_spiele(10000)
