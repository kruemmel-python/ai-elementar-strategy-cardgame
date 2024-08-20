import csv
import random

# Definition der Karten und Elemente
# Es gibt vier Elemente: Feuer, Wasser, Erde, Luft
# Es gibt acht verschiedene Werte für jede Karte: 7, 8, 9, 10, Bube, Dame, König, Ass
ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft"]
WERTE = ["7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]
ANZAHL_ELEMENTAR_PUNKTE = 5  # Jeder Spieler startet mit 5 Elementar-Tokens

# Funktion zur Generierung eines Decks
def deck_generieren():
    # Erzeugt ein Deck aus 32 Karten, jede Kombination aus Element und Wert
    deck = [(element, wert) for element in ELEMENTE for wert in WERTE]
    # Mischt das Deck, um eine zufällige Reihenfolge der Karten zu erhalten
    random.shuffle(deck)
    return deck

# Funktion zur Berechnung der aktuellen Spielsituation als Feature
def spielstand_als_feature(spieler_hand, gegner_hand, spieler_token, gegner_token):
    # Diese Funktion wandelt den aktuellen Spielstand in eine für das Modell geeignete Form um
    # Die Handkarten und die Anzahl der Tokens werden als Features gespeichert
    return {
        "spieler_hand": [str(karte) for karte in spieler_hand],  # Konvertiert die Karten in Strings
        "gegner_hand": [str(karte) for karte in gegner_hand],    # Konvertiert die Karten in Strings
        "spieler_token": spieler_token,  # Anzahl der Tokens des Spielers
        "gegner_token": gegner_token     # Anzahl der Tokens des Gegners
    }

# Funktion zur Bestimmung des Gewinners eines Schlages
def bestimme_gewinner(spieler_karte, gegner_karte):
    # Der Gewinner wird durch den Vergleich der Kartenwerte bestimmt
    # Index der Karte im Werte-Array gibt die Stärke der Karte an
    spieler_wert_index = WERTE.index(spieler_karte[1])
    gegner_wert_index = WERTE.index(gegner_karte[1])
    
    # Wenn die Karte des Spielers stärker ist, gewinnt der Spieler
    if spieler_wert_index > gegner_wert_index:
        return "spieler"
    # Wenn die Karte des Gegners stärker ist, gewinnt der Gegner
    elif gegner_wert_index > spieler_wert_index:
        return "gegner"
    else:
        # Bei gleichen Werten kommt es zu einem Unentschieden
        return "unentschieden"

# Funktion zur Anwendung der Element-Effekte
def wende_element_effekt_an(winner, element, spieler_token, gegner_token):
    # Diese Funktion modifiziert die Anzahl der Tokens basierend auf dem Element der Karte und dem Gewinner
    
    if element == "Feuer" and winner == "spieler":
        gegner_token -= 1  # Feuer verringert die Tokens des Gegners
    elif element == "Wasser" and winner == "spieler":
        spieler_token += 1  # Wasser erhöht die Tokens des Spielers
        gegner_token -= 1   # und verringert die Tokens des Gegners
    elif element == "Erde" and winner == "spieler":
        spieler_token += 1  # Erde erhöht die Tokens des Spielers
    elif element == "Luft" and winner == "spieler":
        # Luft könnte eine zusätzliche Karte ziehen (nicht relevant für diese Simulation)
        pass
    elif element == "Feuer" and winner == "gegner":
        spieler_token -= 1  # Feuer verringert die Tokens des Spielers
    elif element == "Wasser" and winner == "gegner":
        gegner_token += 1   # Wasser erhöht die Tokens des Gegners
        spieler_token -= 1  # und verringert die Tokens des Spielers
    elif element == "Erde" and winner == "gegner":
        gegner_token += 1   # Erde erhöht die Tokens des Gegners
    elif element == "Luft" and winner == "gegner":
        # Luft könnte eine zusätzliche Karte ziehen (nicht relevant für diese Simulation)
        pass
    
    return spieler_token, gegner_token  # Gibt die neuen Token-Zahlen zurück

# Funktion, die ein Spiel simuliert und Daten sammelt
def simuliere_spiel():
    # Ein Deck wird generiert und gemischt
    deck = deck_generieren()
    
    # Die ersten 4 Karten gehen an den Spieler, die nächsten 4 an den Gegner
    spieler_hand = deck[:4]
    gegner_hand = deck[4:8]
    
    # Der Rest bildet den Talon (den Stapel der nicht verteilten Karten)
    talon = deck[8:]
    
    # Beide Spieler starten mit der festgelegten Anzahl an Elementar-Tokens
    spieler_token = ANZAHL_ELEMENTAR_PUNKTE
    gegner_token = ANZAHL_ELEMENTAR_PUNKTE
    
    # Hier werden die Daten des Spiels gesammelt
    spiel_daten = []
    
    # Das Spiel läuft so lange, bis ein Spieler keine Tokens mehr hat
    while spieler_token > 0 and gegner_token > 0:
        # Der Spieler wählt zufällig eine Karte aus seiner Hand, falls er noch welche hat
        if spieler_hand:
            spieler_karte = random.choice(spieler_hand)
            spieler_hand.remove(spieler_karte)
        else:
            break  # Wenn keine Karten mehr vorhanden sind, bricht das Spiel ab
        
        # Der Gegner wählt ebenfalls zufällig eine Karte aus seiner Hand
        if gegner_hand:
            gegner_karte = random.choice(gegner_hand)
            gegner_hand.remove(gegner_karte)
        else:
            break  # Wenn keine Karten mehr vorhanden sind, bricht das Spiel ab
        
        # Bestimme den Gewinner des aktuellen Schlages
        winner = bestimme_gewinner(spieler_karte, gegner_karte)
        
        # Anwenden der Effekte basierend auf dem Element der Karte des Spielers
        spieler_token, gegner_token = wende_element_effekt_an(winner, spieler_karte[0], spieler_token, gegner_token)
        
        # Den aktuellen Spielstand als Feature speichern
        spielstand = spielstand_als_feature(spieler_hand, gegner_hand, spieler_token, gegner_token)
        
        # Speichere den Zug und den Spielstand
        spiel_daten.append({
            "spieler_karte": f"{spieler_karte[0]} {spieler_karte[1]}",  # Gespielte Karte des Spielers
            "gegner_karte": f"{gegner_karte[0]} {gegner_karte[1]}",      # Gespielte Karte des Gegners
            "spieler_token": spieler_token,  # Tokens des Spielers nach dem Zug
            "gegner_token": gegner_token,    # Tokens des Gegners nach dem Zug
            "gewinner": winner               # Gewinner des Schlages
        })
        
        # Nachziehen von Karten, falls der Talon noch Karten enthält
        if talon:
            if len(spieler_hand) < 4:  # Spieler zieht nur nach, wenn er weniger als 4 Karten hat
                spieler_hand.append(talon.pop())
            if len(gegner_hand) < 4:  # Gegner zieht nur nach, wenn er weniger als 4 Karten hat
                gegner_hand.append(talon.pop())
    
    return spiel_daten  # Gibt die gesammelten Spieldaten zurück

# Funktion zur Speicherung der Spieldaten in einer CSV-Datei
def speichere_spieldaten_in_csv(spiel_daten, dateiname="Simulationen/spieldaten.csv"):
    # Diese Funktion speichert die gesammelten Spieldaten in einer CSV-Datei
    schluessel = spiel_daten[0].keys()  # Die Spalten der CSV-Datei entsprechen den Schlüsseln der ersten Datenreihe
    with open(dateiname, mode='w', newline='') as file:  # Öffnet die Datei zum Schreiben
        writer = csv.DictWriter(file, fieldnames=schluessel)  # Erstellt einen CSV-Schreiber
        writer.writeheader()  # Schreibt die Kopfzeile in die CSV-Datei
        writer.writerows(spiel_daten)  # Schreibt die Datenreihen in die CSV-Datei

# Mehrere Spiele simulieren und Daten speichern
def generiere_und_speichere_spiele(anzahl_spiele=10000):
    # Diese Funktion simuliert eine bestimmte Anzahl von Spielen und speichert die Ergebnisse
    alle_spiel_daten = []
    for _ in range(anzahl_spiele):
        spiel_daten = simuliere_spiel()  # Simuliere ein einzelnes Spiel
        alle_spiel_daten.extend(spiel_daten)  # Füge die Spieldaten zur Gesamtliste hinzu
    speichere_spieldaten_in_csv(alle_spiel_daten)  # Speichere die gesammelten Daten in einer CSV-Datei

# Beispielaufruf zur Generierung und Speicherung von 10.000 Spielen
generiere_und_speichere_spiele(10000)
