

---

# Elementar-Schlacht

**Elementar-Schlacht** ist ein strategisches Kartenspiel, bei dem Spieler als Elementarmagier gegeneinander antreten und die Kräfte der vier Elemente (Feuer, Wasser, Erde, Luft) nutzen, um ihre Gegner zu besiegen. Das Spiel kann gegen eine KI gespielt werden, die mit einem neuronalen Netzwerk trainiert wurde.

## Inhaltsverzeichnis

- [Über das Projekt](#über-das-projekt)
- [Spielanleitung](#spielanleitung)
  - [Ziel des Spiels](#ziel-des-spiels)
  - [Spielmaterial](#spielmaterial)
  - [Spielablauf](#spielablauf)
  - [Elementareffekte](#elementareffekte)
  - [Spielende](#spielende)
  - [Strategie-Tipps](#strategie-tipps)
- [Installation](#installation)
- [Verwendung](#verwendung)
- [Dateien und Verzeichnisse](#dateien-und-verzeichnisse)
- [Zukünftige Erweiterungen](#zukünftige-erweiterungen)
- [Lizenz](#lizenz)

## Über das Projekt

**Elementar-Schlacht** ist mehr als nur ein Kartenspiel. Es ist ein Projekt, das maschinelles Lernen nutzt, um eine herausfordernde KI zu entwickeln. Spieler können ihre strategischen Fähigkeiten verbessern und gleichzeitig beobachten, wie sich die KI anpasst und verbessert.

## Spielanleitung

### Ziel des Spiels

Ziel des Spiels ist es, als letzter Magier oder letzte Magierin übrig zu bleiben, der oder die noch Elementar-Tokens besitzt. Verliert ein Spieler oder eine Spielerin alle Tokens, so scheidet er oder sie aus.

### Spielmaterial

- **Kartendeck:** 32 Karten
  - **Farben (Elemente):** Feuer, Wasser, Erde, Luft
  - **Werte:** 7, 8, 9, 10, Bube, Dame, König, Ass
- **Elementar-Tokens:** Jede Spielerin und jeder Spieler startet mit 5 Tokens.
- **Talon:** Der Stapel der verbleibenden Karten nach dem Austeilen.

### Spielablauf

1. **Karten ausspielen:** 
   - Zu Beginn jeder Runde wählt der aktive Spieler oder die aktive Spielerin eine Karte aus seiner oder ihrer Hand aus und spielt diese aus.
   - Die KI wählt ebenfalls eine Karte aus ihrer Hand und spielt sie aus.
   
2. **Gewinner des Schlages bestimmen:**
   - Vergleiche die Elemente der ausgespielten Karten. Die Elemente haben eine bestimmte Hierarchie:
     - Wasser schlägt Feuer.
     - Feuer schlägt Erde.
     - Erde schlägt Luft.
     - Luft schlägt Wasser.
   - Wenn die Elemente gleich sind, gewinnt die Karte mit dem höheren Zahlenwert.
   - Wenn die Elemente unterschiedlich sind und die schwächere Karte eine niedrige Zahl (unter 5) hat, während die stärkere Karte eine hohe Zahl (über 5) hat, könnte die schwächere Karte dennoch gewinnen.

3. **Elementareffekte anwenden:** 
   - Der Gewinner des Schlages wendet den Effekt seines Elements an:
     - **Feuer:** Der Gegner verliert 1 Token.
     - **Wasser:** Der Gewinner erhält 1 Token vom Gegner.
     - **Erde:** Der Gewinner erhält 1 zusätzlichen Token.
     - **Luft:** Der Gewinner erhält 2 zusätzliche Tokens.

4. **Kartenverlust und Nachziehen:**
   - Nach dem Ausspielen einer Karte wird diese aus der Hand entfernt.
   - Nach jedem Schlag ziehen die Spieler eine neue Karte vom Talon, wenn sie weniger als 4 Karten auf der Hand haben. Wenn der Talon leer ist, ziehen die Spieler keine Karten mehr nach.

### Elementareffekte

- **Feuer (Rot):** Ein direkter Angriff, bei dem der Gegner Tokens verliert.
- **Wasser (Blau):** Stehlen von Tokens vom Gegner.
- **Erde (Grün):** Selbstschutz durch das Hinzufügen von Tokens.
- **Luft (Gelb):** Doppelte Token-Zunahme für den Gewinner.

### Spielende

Das Spiel endet, wenn einer der folgenden Bedingungen erfüllt ist:
1. Ein Spieler hat keine Karten mehr auf der Hand.
2. Ein Spieler hat keine Elementar-Tokens mehr.

### Strategie-Tipps

- **Hierarchie beachten:** Kenne die Hierarchie der Elemente gut und plane deine Züge entsprechend.
- **Zahlenwertstrategie:** Behalte im Auge, welche Zahlenwerte du noch auf der Hand hast.
- **Tokens verwalten:** Sei vorsichtig mit deinen Tokens und versuche, den Gegner gezielt zu schwächen.

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

## Lizenz

Dieses Projekt steht unter der [MIT-Lizenz](LICENSE). Siehe die `LICENSE`-Datei für weitere Details.

