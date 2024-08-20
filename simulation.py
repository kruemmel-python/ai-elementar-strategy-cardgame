import csv
import random

# Definition der Karten und Elemente
ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft"]
WERTE = ["7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]
ANZAHL_ELEMENTAR_PUNKTE = 5

# Funktion zur Generierung eines Decks
def deck_generieren():
    deck = [(element, wert) for element in ELEMENTE for wert in WERTE]
    random.shuffle(deck)
    return deck

# Funktion zur Berechnung der aktuellen Spielsituation als Feature
def spielstand_als_feature(spieler_hand, gegner_hand, spieler_token, gegner_token):
    return {
        "spieler_hand": [str(karte) for karte in spieler_hand],
        "gegner_hand": [str(karte) for karte in gegner_hand],
        "spieler_token": spieler_token,
        "gegner_token": gegner_token
    }

# Funktion zur Bestimmung des Gewinners eines Schlages
def bestimme_gewinner(spieler_karte, gegner_karte):
    spieler_wert_index = WERTE.index(spieler_karte[1])
    gegner_wert_index = WERTE.index(gegner_karte[1])
    if spieler_wert_index > gegner_wert_index:
        return "spieler"
    elif gegner_wert_index > spieler_wert_index:
        return "gegner"
    else:
        return "unentschieden"

# Funktion zur Anwendung der Element-Effekte
def wende_element_effekt_an(winner, element, spieler_token, gegner_token):
    if element == "Feuer" and winner == "spieler":
        gegner_token -= 1
    elif element == "Wasser" and winner == "spieler":
        spieler_token += 1
        gegner_token -= 1
    elif element == "Erde" and winner == "spieler":
        spieler_token += 1
    elif element == "Luft" and winner == "spieler":
        # Spieler könnte eine zusätzliche Karte ziehen (hier nicht relevant für die Simulation)
        pass
    elif element == "Feuer" and winner == "gegner":
        spieler_token -= 1
    elif element == "Wasser" and winner == "gegner":
        gegner_token += 1
        spieler_token -= 1
    elif element == "Erde" and winner == "gegner":
        gegner_token += 1
    elif element == "Luft" and winner == "gegner":
        # Gegner könnte eine zusätzliche Karte ziehen (hier nicht relevant für die Simulation)
        pass
    return spieler_token, gegner_token

# Funktion, die ein Spiel simuliert und Daten sammelt
def simuliere_spiel():
    deck = deck_generieren()
    spieler_hand = deck[:4]
    gegner_hand = deck[4:8]
    talon = deck[8:]
    
    spieler_token = ANZAHL_ELEMENTAR_PUNKTE
    gegner_token = ANZAHL_ELEMENTAR_PUNKTE
    
    spiel_daten = []
    
    while spieler_token > 0 and gegner_token > 0:
        if spieler_hand:  # Nur wählen, wenn Karten vorhanden sind
            spieler_karte = random.choice(spieler_hand)
            spieler_hand.remove(spieler_karte)
        else:
            break
        
        if gegner_hand:  # Nur wählen, wenn Karten vorhanden sind
            gegner_karte = random.choice(gegner_hand)
            gegner_hand.remove(gegner_karte)
        else:
            break
        
        # Bestimme den Gewinner des Schlages
        winner = bestimme_gewinner(spieler_karte, gegner_karte)
        
        # Anwenden des Effekts basierend auf dem Element der Karte
        spieler_token, gegner_token = wende_element_effekt_an(winner, spieler_karte[0], spieler_token, gegner_token)
        
        # Spielstand sammeln
        spielstand = spielstand_als_feature(spieler_hand, gegner_hand, spieler_token, gegner_token)
        spiel_daten.append({
            "spieler_karte": f"{spieler_karte[0]} {spieler_karte[1]}",
            "gegner_karte": f"{gegner_karte[0]} {gegner_karte[1]}",
            "spieler_token": spieler_token,
            "gegner_token": gegner_token,
            "gewinner": winner
        })
        
        # Karten nachziehen, wenn noch Karten im Talon sind
        if talon:
            if len(spieler_hand) < 4:
                spieler_hand.append(talon.pop())
            if len(gegner_hand) < 4:
                gegner_hand.append(talon.pop())
    
    return spiel_daten

# Funktion zur Speicherung der Spieldaten in einer CSV-Datei
def speichere_spieldaten_in_csv(spiel_daten, dateiname="Simulationen/spieldaten.csv"):
    schluessel = spiel_daten[0].keys()
    with open(dateiname, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=schluessel)
        writer.writeheader()
        writer.writerows(spiel_daten)

# Mehrere Spiele simulieren und Daten speichern
def generiere_und_speichere_spiele(anzahl_spiele=10000):
    alle_spiel_daten = []
    for _ in range(anzahl_spiele):
        spiel_daten = simuliere_spiel()
        alle_spiel_daten.extend(spiel_daten)
    speichere_spieldaten_in_csv(alle_spiel_daten)

# Beispielaufruf zur Generierung und Speicherung von 100 Spielen
generiere_und_speichere_spiele(10000)
