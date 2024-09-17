# Modellbeschreibung: Elementar-Schlacht

Dieses Dokument beschreibt das Modell, das in **Elementar-Schlacht** verwendet wird, um die KI im Spiel zu steuern. Das Modell wurde mithilfe von **Keras** und **TensorFlow** implementiert und ist darauf ausgelegt, strategische Entscheidungen zu treffen, basierend auf der aktuellen Spielsituation.

## 📊 Modellstruktur

### Eingabedaten

Das Modell erhält als Eingabe eine kodierte Darstellung der aktuellen Spielsituation, die folgende Informationen umfasst:

- **Spielerkarte (Element, Wert):** Das Element und der Wert der vom Spieler gewählten Karte.
- **Karte der KI (Element, Wert):** Das Element und der Wert der von der KI gewählten Karte.
- **Tokens:** Die Anzahl der verbleibenden Tokens sowohl für den Spieler als auch für die KI.
- **Wettereffekte:** Kodierte Wetterbedingungen (z.B. Regen, Windsturm, Erdbeben), die die aktuellen Karten beeinflussen.
- **Helden:** Der aktuell gespielte Held (Spieler und KI) und der damit verbundene Elementbonus.

Diese Eingabedaten werden als numerischer Vektor in das Modell eingespeist, um die Spielsituation vollständig abzubilden. Jedes dieser Features wird vorab durch **Label-Encoding** und **One-Hot-Encoding** in numerische Werte umgewandelt.

### Architektur

Das neuronale Netzwerk ist so konzipiert, dass es die komplexen Interaktionen zwischen Karten, Tokens, Wetter und Helden erfasst, um die bestmögliche Entscheidung für die KI zu treffen.

- **Eingabeschicht:** Nimmt die kodierten numerischen Werte der Spielsituation entgegen.
- **Verborgene Schichten:** Mehrere dichte (Dense) Schichten, die über **ReLU**-Aktivierungsfunktionen nicht-lineare Beziehungen modellieren. Dies ermöglicht dem Modell, die komplexen Zusammenhänge zwischen den Elementen, Tokens, Wetterbedingungen und Heldenbonis zu erkennen.
- **Ausgabeschicht:** Liefert die Wahrscheinlichkeit aus, mit der die KI den aktuellen Schlag gewinnt.

### Ausgabedaten

Das Modell gibt eine Wahrscheinlichkeit (zwischen 0 und 1) aus, die angibt, wie wahrscheinlich es ist, dass die KI den aktuellen Schlag gewinnt. Diese Wahrscheinlichkeit wird genutzt, um die Karte zu bestimmen, die am ehesten zu einem Sieg führt.

## 🏋️ Training des Modells

### Daten

Das Modell wird mit simulierten Spieldaten trainiert, die durch zahlreiche Spiele zwischen der KI und einem virtuellen Gegner generiert wurden. Die Trainingsdaten bestehen aus:

- **Eingabedaten:** Die Karten (Elemente und Werte), Tokens, Wetterbedingungen und Helden, die in der aktuellen Spielsituation vorliegen.
- **Zielvariable:** Der Gewinner des Schlages (Spieler oder KI), basierend auf den Regeln des Spiels und den Elementar- und Heldenbonussen.

### Optimierung

Das Modell wird unter Verwendung des **Adam**-Optimierers trainiert, um die Fehlerrate zu minimieren und die Vorhersagegenauigkeit zu maximieren. 

- **Lernrate:** Dynamisch angepasst, um einen optimalen Lernprozess zu gewährleisten.
- **Early Stopping:** Wird verwendet, um zu verhindern, dass das Modell zu stark auf die Trainingsdaten angepasst wird (Overfitting). Dadurch bleibt es auf neue Spielsituationen anwendbar.

Das Modell wird über mehrere Epochen trainiert, bis es eine gute Balance zwischen Genauigkeit und Generalisierungsfähigkeit erreicht hat.

## 🎮 Einsatz im Spiel

Nach dem Training wird das Modell in das Hauptspiel integriert und in Echtzeit verwendet. Die KI greift auf das trainierte Modell zu, um anhand der aktuellen Spielsituation die beste Entscheidung zu treffen. Der Entscheidungsprozess umfasst:

1. **Einspeisen der aktuellen Spielsituation** (Spielerkarten, KI-Karten, Tokens, Wetter, Helden).
2. **Vorhersage der Gewinnwahrscheinlichkeit** für die KI.
3. **Auswahl der optimalen Karte**, die am ehesten zu einem Sieg führt, basierend auf der Modellvorhersage.

Dadurch bleibt das Spiel dynamisch und bietet eine herausfordernde Erfahrung für die Spieler.

---

### 📂 Dateistruktur

- **`elementar_schlacht_modell.keras`**: Das trainierte Modell im Keras-Format.
- **`training.py`**: Skript zum Training des Modells.
- **`simulation.py`**: Skript zur Generierung von Trainingsdaten.
- **`spiel.py`**: Hauptspiel-Skript, in dem das Modell verwendet wird.

---

Dieses Modell ermöglicht es der KI, sich flexibel an verschiedene Spielsituationen anzupassen und sorgt dafür, dass *Elementar-Schlacht* eine interessante und dynamische Herausforderung bleibt.
