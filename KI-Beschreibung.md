# Modellbeschreibung: Elementar-Schlacht

Dieses Dokument beschreibt das Modell, das in **Elementar-Schlacht** verwendet wird, um die KI im Spiel zu steuern. Das Modell wurde mithilfe von **Keras** und **TensorFlow** implementiert und ist darauf ausgelegt, strategische Entscheidungen zu treffen, basierend auf der aktuellen Spielsituation.

## 📊 Modellstruktur

### Eingabedaten

Das Modell erhält als Eingabe eine kodierte Darstellung der aktuellen Spielsituation, die folgende Informationen umfasst:

- **Karten:** Die Karten, die der Spieler und die KI aktuell auf der Hand haben.
- **Tokens:** Die Anzahl der verbleibenden Tokens sowohl für den Spieler als auch für die KI.

Diese Daten werden als numerischer Vektor in das Modell eingespeist, um die Spielsituation zu beschreiben.

### Architektur

Das neuronale Netzwerk besteht aus mehreren dichten Schichten (Dense Layers), die die Eingabedaten verarbeiten. Die Architektur ist so konzipiert, dass sie komplexe Muster in den Daten erkennt, die der KI helfen, optimale Entscheidungen zu treffen.

- **Aktivierungsfunktionen:** Es werden **ReLU**-Aktivierungsfunktionen verwendet, um nicht-lineare Beziehungen zu modellieren.
- **Schichten:** Das Modell verwendet mehrere Schichten, um die Eingaben in Zwischenrepräsentationen umzuwandeln, die schließlich zur Vorhersage führen.

### Ausgabedaten

Das Modell gibt eine Wahrscheinlichkeit aus, die angibt, wie wahrscheinlich es ist, dass die KI den aktuellen Schlag gewinnt. Diese Wahrscheinlichkeit hilft der KI, die Karte zu wählen, die am wahrscheinlichsten zu einem Sieg führt.

## 🏋️ Training des Modells

### Daten

Das Modell wird mit simulierten Spieldaten trainiert, die durch zahlreiche Spiele zwischen der KI und einem virtuellen Gegner generiert wurden. Jedes Spiel liefert:

- **Eingaben:** Die Karten und Tokens in der aktuellen Spielsituation.
- **Zielvariable:** Der Gewinner des Schlages (Spieler oder KI).

### Optimierung

Das Modell wird mit dem **Adam**-Optimierer trainiert, um die Fehlerrate zu minimieren. Das Training erfolgt über mehrere Epochen, wobei:

- **Lernrate:** Automatisch angepasst wird, um die Genauigkeit zu verbessern.
- **Early Stopping:** Verwendet wird, um das Modell vor Überanpassung (Overfitting) zu schützen.

## 🎮 Einsatz im Spiel

Nach dem Training wird das Modell im Spiel eingesetzt, um in Echtzeit Vorhersagen zu treffen und der KI zu helfen, die besten Entscheidungen zu treffen. Dadurch bleibt das Spiel dynamisch und herausfordernd.

---

### 📂 Dateistruktur

- **`elementar_schlacht_modell.keras`**: Das trainierte Modell im Keras-Format.
- **`training.py`**: Skript zum Training des Modells.
- **`simulation.py`**: Skript zur Generierung von Trainingsdaten.
- **`spiel.py`**: Hauptspiel-Skript, in dem das Modell verwendet wird.

---

Dieses Modell ermöglicht es der KI, sich flexibel an verschiedene Spielsituationen anzupassen und sorgt dafür, dass *Elementar-Schlacht* eine interessante und dynamische Herausforderung bleibt.

