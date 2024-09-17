
# Elementar-Schlacht


**Elementar-Schlacht** ist ein strategisches Kartenspiel, bei dem Spieler als Elementarmagier gegeneinander antreten und die Kräfte der sieben Elemente (Feuer, Wasser, Erde, Luft, Blitz, Eis, Magie) nutzen, um ihre Gegner zu besiegen. Das Spiel kann gegen eine KI gespielt werden, die mit einem neuronalen Netzwerk trainiert wurde.

## Inhaltsverzeichnis

- [Über das Projekt](#über-das-projekt)
- [Spielanleitung](#spielanleitung)
  - [Ziel des Spiels](#ziel-des-spiels)
  - [Spielmaterial](#spielmaterial)
  - [Spielablauf](#spielablauf)
  - [Elementareffekte](#elementareffekte)
  - [Heldenboni](#heldenboni)
  - [Wettereffekte](#wettereffekte)
  - [Spielende](#spielende)
  - [Strategie-Tipps](#strategie-tipps)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Dateien und Verzeichnisse](#dateien-und-verzeichnisse)
- [Zukünftige Erweiterungen](#zukünftige-erweiterungen)
- [Lizenz](#lizenz)

## Über das Projekt

**Elementar-Schlacht** kombiniert klassische Kartenspiele mit moderner KI. Durch den Einsatz von maschinellem Lernen wird die Herausforderung durch eine lernende und anpassungsfähige KI gesteigert. Zusätzlich wurden Helden, neue Elemente und Wettereffekte eingeführt, um das Spielerlebnis noch dynamischer und strategischer zu gestalten.

## Spielanleitung

### Ziel des Spiels

Das Ziel des Spiels ist es, der letzte Magier oder die letzte Magierin zu sein, der oder die noch Elementar-Tokens besitzt. Verliert ein Spieler alle Tokens, scheidet er aus.

### Spielmaterial

- **Kartendeck:** 49 Karten
  - **Elemente:** Feuer, Wasser, Erde, Luft, Blitz, Eis, Magie
  - **Werte:** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, Bube, Dame, König, Ass
- **Elementar-Tokens:** Jeder Spieler startet mit 5 Tokens.
- **Heldenkarten:** Jeder Spieler erhält einen zufälligen Helden mit einem speziellen Elementbonus.
- **Talon:** Der Stapel der verbleibenden Karten nach dem Austeilen.
- **Wettereffekte:** Zu Beginn jeder Runde wird ein zufälliges Wetterereignis ausgewählt, das die Schlacht beeinflusst.

### Spielablauf

1. **Karten ausspielen:** 
   - Zu Beginn jeder Runde wählt der aktive Spieler eine Karte aus seiner Hand aus.
   - Die KI wählt ebenfalls eine Karte aus ihrer Hand.
   
2. **KI denkt nach:** 
   - Bevor die KI ihre Karte spielt, wird ein Symbol angezeigt, das ca. 3 Sekunden lang rotiert. Dies erhöht die Spannung und simuliert das "Nachdenken" der KI.
   
3. **Auswertung des Schlages:**
   - Vergleiche die Elemente der ausgespielten Karten:
     - **Wasser schlägt Feuer.**
     - **Feuer schlägt Erde.**
     - **Erde schlägt Luft.**
     - **Luft schlägt Wasser.**
     - **Magie** und **Blitz** haben spezielle Interaktionen und Boni.
   - Wenn die Elemente gleich sind, gewinnt die Karte mit dem höheren Zahlenwert.
   - **Elementboni:** Jeder Schlag erhält basierend auf der Interaktion der Elemente Boni oder Malusse.
   - **Heldenboni:** Jeder Held hat einen spezifischen Bonus für sein Element. Wird eine Karte gespielt, die dem Element des Helden entspricht, erhält der Spieler einen zusätzlichen Bonus (z.B. der Drache erhält +2 für Feuerkarten).
   - **Tokenboni:** Die Anzahl der Tokens beeinflusst ebenfalls das Ergebnis, basierend auf einer gestaffelten Bonusregel (z.B. +2 Tokenbonus bei 5 Tokens).
  
4. **Elementareffekte anwenden:** 
   - Der Gewinner wendet den Effekt seines Elements an:
     - **Feuer:** Der Gegner verliert 1 Token.
     - **Wasser:** Der Gewinner erhält 1 Token vom Gegner.
     - **Erde:** Der Gewinner erhält 1 zusätzlichen Token.
     - **Luft:** Der Gewinner erhält 2 zusätzliche Tokens.
     - **Blitz:** Starke Angriffe, die verschiedene Elemente übertreffen können.
     - **Eis:** Kann gegnerische Effekte abschwächen.
     - **Magie:** Universelle Effekte, die Boni gegen alle Elemente bieten.

5. **Wettereffekte berücksichtigen:** 
   - Jedes Wetterereignis kann die Dynamik des Spiels beeinflussen:
     - **Regen:** Verstärkt Wasser und schwächt Feuer.
     - **Windsturm:** Verstärkt Luft und schwächt Erde.
     - **Erdbeben:** Hat eine ausgeglichene, aber schwächende Wirkung auf alle Elemente.

6. **Kartenverlust und Nachziehen:**
   - Nach dem Ausspielen einer Karte wird diese aus der Hand entfernt.
   - Nach jedem Schlag ziehen die Spieler eine neue Karte vom Talon, falls sie weniger als 4 Karten auf der Hand haben.

### Elementareffekte

- **Feuer (Rot):** Gegner verliert Tokens.
- **Wasser (Blau):** Stehlen von Tokens vom Gegner.
- **Erde (Grün):** Selbstschutz durch das Hinzufügen von Tokens.
- **Luft (Gelb):** Doppelte Token-Zunahme für den Gewinner.
- **Blitz (Violett):** Unvorhersehbare Angriffe, die verschiedene Elemente schlagen können.
- **Eis (Weiß):** Abschwächen von gegnerischen Karten und Effekten.
- **Magie (Lila):** Starke universelle Boni gegen alle Elemente.

### Heldenboni

Jeder Spieler hat einen Helden, der einen Bonus für sein Element erhält:

- **Drache:** +2 Bonus auf **Feuer**-Karten.
- **Zauberer:** +3 Bonus auf **Magie**-Karten.

Wenn ein Spieler eine Karte spielt, die dem Element seines Helden entspricht, wird dieser Bonus dem Gesamtwert der Karte hinzugefügt.

### Wettereffekte

- **Regen:** +1 auf Wasser, -1 auf Feuer.
- **Windsturm:** +2 auf Luft, -1 auf Erde.
- **Erdbeben:** Schwächt alle Kartenwerte um 1.

### Spielende

Das Spiel endet, wenn einer der folgenden Bedingungen erfüllt ist:
1. Ein Spieler hat keine Karten mehr auf der Hand.
2. Ein Spieler hat keine Elementar-Tokens mehr.

### Strategie-Tipps

- **Element-Hierarchie beachten:** Plane deine Züge unter Berücksichtigung der Element-Hierarchie.
- **Heldenboni nutzen:** Nutze den Bonus deines Helden, indem du Karten seines Elements spielst.
- **Wettereffekte berücksichtigen:** Spiele deine Karten so, dass du von den Wettereffekten profitierst.
- **Tokens verwalten:** Achte auf deine Tokens, denn sie können dir entscheidende Vorteile verschaffen.

## Installation

Um **Elementar-Schlacht** lokal auszuführen, führe die folgenden Schritte aus:

1. **Repository klonen:**
   ```bash
   git clone https://github.com/kruemmel-python/ai-elementar-strategy-cardgame.git
   cd elementar-schlacht
   ```

2. **Virtuelle Umgebung erstellen:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/MacOS
   venv\Scripts\activate  # Windows
   ```

3. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

## Verwendung

### 1. Simulation von Spielen
Führe die Simulationen durch, um Daten zu generieren, die das Modell trainieren:
```bash
python simulation.py
```

### 2. Training des Modells
Trainiere das KI-Modell mit den simulierten Daten:
```bash
python training.py
```

### 3. Spiel gegen die KI
Starte das Spiel und spiele gegen die KI:
```bash
python spiel.py
```

## Dateien und Verzeichnisse

- **`spiel.py`**: Das Hauptspiel-Skript, mit dem du gegen die KI spielen kannst.
- **`simulation.py`**: Skript zur Simulation von Spielen und Erzeugung von Trainingsdaten.
- **`training.py`**: Skript zum Trainieren des KI-Modells mit den generierten Daten.
- **`Simulationen/`**: Ordner, in dem die simulierten Spieldaten und das trainierte Modell gespeichert werden.

## Zukünftige Erweiterungen

- **Mehrspieler-Modus:** Füge einen Modus hinzu, in dem mehrere menschliche Spieler gegeneinander antreten können.
- **Erweiterte KI:** Verbesserung des KI-Modells für eine stärkere Herausforderung.
- **Neue Karten und Elemente:** Einführung neuer Kartentypen und -effekte, um das Spiel noch spannender zu gestalten.



