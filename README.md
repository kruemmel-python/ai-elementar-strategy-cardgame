# Elementar-Schlacht
![image](https://github.com/user-attachments/assets/1e42957f-e25b-4d47-94e0-2ffebea1ef23)

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

**Elementar-Schlacht** ist mehr als nur ein Kartenspiel. Es ist ein Projekt, das maschinelles Lernen nutzt, um eine herausfordernde KI zu entwickeln. Spieler können ihre strategischen Fähigkeiten verbessern und gleichzeitig beobachten, wie sich die KI anpasst und verbessert. Neue spannende Spielelemente wurden hinzugefügt, um das Spielerlebnis fesselnder zu machen.

## Spielanleitung

### Ziel des Spiels

Ziel des Spiels ist es, als letzter Magier oder letzte Magierin übrig zu bleiben, der oder die noch Elementar-Tokens besitzt. Verliert ein Spieler oder eine Spielerin alle Tokens, so scheidet er oder sie aus.

### Spielmaterial

- **Kartendeck:** 32 Karten
  - **Farben (Elemente):** Feuer, Wasser, Erde, Luft
  - **Werte:** 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, Bube, Dame, König, Ass
- **Elementar-Tokens:** Jede Spielerin und jeder Spieler startet mit 5 Tokens.
- **Talon:** Der Stapel der verbleibenden Karten nach dem Austeilen.

### Spielablauf

1. **Karten ausspielen:** 
   - Zu Beginn jeder Runde wählt der aktive Spieler oder die aktive Spielerin eine Karte aus seiner oder ihrer Hand aus und spielt diese aus.
   - Die KI wählt ebenfalls eine Karte aus ihrer Hand und spielt sie aus.
   
2. **Spannung und Verzögerung:** 
   - Bevor die KI ihre Karte spielt, erscheint eine Nachricht, dass die KI "nachdenkt", begleitet von einem rotierenden Symbol, das ca. 3 Sekunden lang sichtbar ist. Dies erhöht die Spannung.
   - Nachdem die KI ihre Karte ausgespielt hat, folgt die Nachricht "Spiel wird analysiert", die ebenfalls von einer kurzen Pause und einem sich drehenden Symbol begleitet wird.

3. **Gewinner des Schlages bestimmen:**
   - Vergleiche die Elemente der ausgespielten Karten. Die Elemente haben eine bestimmte Hierarchie:
     - Wasser schlägt Feuer.
     - Feuer schlägt Erde.
     - Erde schlägt Luft.
     - Luft schlägt Wasser.
   - Wenn die Elemente gleich sind, gewinnt die Karte mit dem höheren Zahlenwert.
   - Elementboni: Jeder Schlag erhält einen Elementbonus (oder -malus), basierend auf der Interaktion der Elemente. Ein direktes Übertrumpfen führt zu einem größeren Bonus (z.B. +3), während neutrale Interaktionen kleinere Boni (z.B. +1) oder Malusse (z.B. -1) erhalten.
   - Auch die Anzahl der Tokens hat einen Einfluss auf das Ergebnis. Spieler und KI erhalten Tokenboni, die ihren Gesamtwert im Spiel beeinflussen.
  
   - ![image](https://github.com/user-attachments/assets/90a915e1-611b-4d6c-99f5-975edbbe1496)


4. **Elementareffekte anwenden:** 
   - Der Gewinner des Schlages wendet den Effekt seines Elements an:
     - **Feuer:** Der Gegner verliert 1 Token.
     - **Wasser:** Der Gewinner erhält 1 Token vom Gegner.
     - **Erde:** Der Gewinner erhält 1 zusätzlichen Token.
     - **Luft:** Der Gewinner erhält 2 zusätzliche Tokens.

5. **Kartenverlust und Nachziehen:**
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
- **Spannung nutzen:** Die verzögerten Aktionen der KI geben dir Zeit, deine eigene Strategie zu überdenken, bevor das Ergebnis angezeigt wird.

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

Dieses Projekt steht unter der [MIT-Lizenz]([LICENSE](https://github.com/kruemmel-python/ai-elementar-strategy-cardgame/blob/main/LICENSE.md)). Siehe die `LICENSE`-Datei für weitere Details.

