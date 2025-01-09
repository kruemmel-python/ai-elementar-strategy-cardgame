# Elementar Schlacht - Kartenspiel

## Übersicht

**Elementar Schlacht** ist ein strategisches Kartenspiel, das mithilfe von Python entwickelt wurde. Es bietet eine interaktive grafische Benutzeroberfläche (GUI), bei der der Spieler gegen eine KI antreten kann. Die Karten sind nach Elementen kategorisiert (z. B. Feuer, Wasser, Erde) und bieten unterschiedliche Werte sowie Boni.

Das Projekt wurde modular aufgebaut, um eine klare Struktur zu gewährleisten. Es umfasst sowohl Spielmechaniken als auch grafische Darstellungen.

---

## Inhaltsverzeichnis

1. [Features](#features)
2. [Installation](#installation)
3. [Verwendung](#verwendung)
4. [Projektstruktur](#projektstruktur)
5. [Technische Details](#technische-details)
6. [Screenshots](#screenshots)
7. [Credits](#credits)

---

## Features

- **Grafische Benutzeroberfläche (GUI):** Intuitive Bedienung des Spiels über eine interaktive Oberfläche.
- **Kartenmechanik:** Verschiedene Elemente und Kartenwerte beeinflussen das Spiel.
- **KI-Gegner:** Automatische Gegnerlogik, die Entscheidungen basierend auf den Karten trifft.
- **Wettereffekte:** Zufällige Modifikatoren, die die Spielmechanik beeinflussen.
- **Simulationen:** Training und Simulation der Kartenstrategien mit gespeicherten Daten.

---

## Installation

### Voraussetzungen

- Python 3.12 oder höher
- Die folgenden Python-Bibliotheken müssen installiert sein:
  - `tkinter`
  - `Pillow`

### Schritte

1. **Repository klonen oder herunterladen:**
   ```bash
   git clone https://github.com/kruemmel-python/ai-elementar-strategy-cardgame/elementar-schlacht.git
   ```

2. **In das Projektverzeichnis wechseln:**
   ```bash
   cd elementar-schlacht
   ```

3. **Abhängigkeiten installieren:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Spiel starten:**
   ```bash
   python gui.py
   ```

---

## Verwendung

1. **Spiel starten:** Führen Sie die Datei `gui.py` aus, um die grafische Benutzeroberfläche zu öffnen.
2. **Karten auswählen:** Wählen Sie Karten aus Ihrer Hand und spielen Sie gegen die KI.
3. **Strategie:** Nutzen Sie die Boni Ihrer Helden und die Elemente der Karten.
4. **Spiel beenden:** Das Spiel endet, wenn ein Spieler keine Karten mehr hat oder alle Runden abgeschlossen sind.

---

## Projektstruktur

```
.
├── gui.py                 # Hauptdatei für die grafische Oberfläche
├── spiel.py               # Spielmechanik und Regeln
├── konstanten.py          # Definiert Konfigurationswerte wie Kartenpfade
├── create_cards.py        # Logik zur Erstellung von Karten
├── Simulationen/          # Daten und Modelle für Simulationen
├── PNG/Cards/             # Ressourcen für Kartenbilder
└── README.md              # Dokumentation
```

---

## Technische Details

- **GUI:** Entwickelt mit `tkinter` für eine benutzerfreundliche Oberfläche.
- **Kartenbilder:** Verwendet `Pillow`, um Bilder dynamisch zu laden und anzuzeigen.
- **Spielmechanik:** Die Regeln und Logik des Spiels sind in `spiel.py` definiert.
- **KI:** Enthält eine einfache Strategie, die auf den Kartenwerten und Elementen basiert.

### Simulationen
Das Projekt enthält Simulationen, die in `Simulationen/spieldaten.csv` gespeichert sind. Diese Daten können genutzt werden, um Modelle weiter zu trainieren.

---

## Screenshots

### Hauptmenü
![Hauptmenü](game_as_module/gui1.png)

### Spielerhand
![Spielerhand](game_as_module/gui2.png)

### Spielstatus
![Spielstatus](game_as_module/gui3.png)

---

## Credits

- **Entwicklung:** Ralf Krümmeö
- **Ressourcen:** Kartenbilder und weitere Ressourcen aus lizenzfreien Quellen

---


