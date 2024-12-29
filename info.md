# Elementar Schlacht Modell

Dieses Repository enthält den Code und die Daten für das Training eines KI-Modells, das die Ergebnisse von Schlachten zwischen verschiedenen Elementen vorhersagt. Das Modell wird mit Daten trainiert, die verschiedene Spieler- und Gegnerkarten, Wetterbedingungen und Heldeninformationen enthalten.

## Inhalt

- `training.log`: Log-Datei, die den Trainingsprozess dokumentiert.
- `Simulationen/spieldaten.csv`: CSV-Datei mit den Spieldaten.
- `Simulationen/elementar_schlacht_modell.keras`: Gespeichertes Keras-Modell.
- `train_model.py`: Python-Skript zum Trainieren des Modells.

## Wie funktioniert das Training der KI genau?

Das Training der KI erfolgt in mehreren Schritten:

1. **Datenladen**: Die Spieldaten werden aus einer CSV-Datei geladen.
2. **Datenvorverarbeitung**: Die Daten werden vorverarbeitet, indem kategorische Merkmale kodiert und die Daten in Trainings- und Testsets aufgeteilt werden.
3. **ModellErstellung**: Ein neuronales Netzwerk wird erstellt.
4. **Modelltraining**: Das Modell wird trainiert, wobei optional eine Hyperparameter-Optimierung durchgeführt werden kann.
5. **Modellbewertung**: Das trainierte Modell wird bewertet und die Ergebnisse werden ausgegeben.

### Datenladen

Die Spieldaten werden aus der Datei `Simulationen/spieldaten.csv` geladen. Falls die Datei nicht gefunden wird, wird ein Fehler protokolliert und das Programm beendet.

### Datenvorverarbeitung

Die Daten werden vorverarbeitet, indem:

- Die Spieler- und Gegnerkarten in Elemente und Werte aufgeteilt werden.
- Die Elemente und Werte mit `LabelEncoder` kodiert werden.
- Das Wetter und die Helden mit `OneHotEncoder` kodiert werden.
- Die kodierten Daten in einem DataFrame zusammengeführt werden.
- Die Gewinnerlabels mit `LabelEncoder` kodiert werden.

### ModellErstellung

Ein neuronales Netzwerk wird mit der folgenden Architektur erstellt:

- Eingabeschicht mit einer festgelegten Anzahl von Einheiten.
- Zwei verborgene Schichten mit ReLU-Aktivierungsfunktionen.
- Eine Ausgabeschicht mit Softmax-Aktivierungsfunktion für die Klassifikation.

### Modelltraining

Das Modell wird mit den Trainingsdaten trainiert. Optional kann eine Hyperparameter-Optimierung mit `GridSearchCV` durchgeführt werden, um die besten Hyperparameter zu finden. Während des Trainings werden Callbacks wie `EarlyStopping` und `ReduceLROnPlateau` verwendet, um Überanpassung zu vermeiden und die Lernrate anzupassen.

### Modellbewertung

Nach dem Training wird das Modell bewertet, indem:

- Die Testgenauigkeit berechnet wird.
- Ein Klassifikationsbericht erstellt wird.

## Welche Technologien und Frameworks kommen zum Einsatz?

Für das Training und die Bewertung des Modells werden verschiedene Technologien und Frameworks verwendet:

- **Python**: Die Programmiersprache, in der das Skript geschrieben ist.
- **Pandas**: Für die Datenmanipulation und -analyse.
- **NumPy**: Für numerische Berechnungen.
- **Scikit-learn**: Für die Datenvorverarbeitung und die Hyperparameter-Optimierung.
- **TensorFlow/Keras**: Für die Erstellung und das Training des neuronalen Netzwerks.
- **Matplotlib**: Für die Visualisierung der Trainingsverläufe.
- **Scikeras**: Für die Integration von Keras-Modellen in Scikit-learn.

## Welche Einschränkungen oder Grenzen hat die KI?

Obwohl das Modell in der Lage ist, die Ergebnisse von Schlachten vorherzusagen, gibt es einige Einschränkungen und Grenzen:

1. **Datenabhängigkeit**: Die Genauigkeit des Modells hängt stark von der Qualität und Menge der Trainingsdaten ab. Unvollständige oder fehlerhafte Daten können die Vorhersagen beeinträchtigen.
2. **Überanpassung**: Das Modell könnte überanpassen, insbesondere wenn die Trainingsdaten nicht repräsentativ für alle möglichen Szenarien sind.
3. **Generalität**: Das Modell ist speziell auf die vorliegenden Daten trainiert. Es ist möglicherweise nicht in der Lage, neue oder unbekannte Szenarien genau vorherzusagen.
4. **Interpretierbarkeit**: Neuronale Netzwerke sind oft schwer zu interpretieren. Es kann schwierig sein, genau zu verstehen, warum das Modell bestimmte Vorhersagen trifft.
5. **Ressourcenbedarf**: Das Training eines neuronalen Netzwerks kann rechenintensiv sein und erfordert möglicherweise leistungsstarke Hardware.

## Verwendung

Um das Modell zu trainieren, führen Sie das Skript `train_model.py` aus:

```bash
python train_model.py
```

## Abhängigkeiten

Die folgenden Python-Bibliotheken werden benötigt:

- `csv`
- `random`
- `pathlib`
- `logging`
- `os`
- `pandas`
- `numpy`
- `sklearn`
- `tensorflow`
- `matplotlib`
- `scikeras`

Installieren Sie die erforderlichen Bibliotheken mit:

```bash
pip install pandas numpy scikit-learn tensorflow matplotlib scikeras
```

## Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert. Weitere Informationen finden Sie in der Datei `LICENSE`.

## Kontakt

Für Fragen oder Anregungen kontaktieren Sie bitte den Autor dieses Repositorys.
