import os  # Bibliothek zum Arbeiten mit dem Betriebssystem, z.B. zum Überprüfen von Dateipfaden
import pandas as pd  # Pandas wird verwendet, um die CSV-Datei zu laden und zu verarbeiten
import numpy as np  # Numpy wird für numerische Operationen verwendet
from sklearn.model_selection import train_test_split  # Zum Aufteilen der Daten in Trainings- und Testsets
from sklearn.preprocessing import LabelEncoder  # Zum Umwandeln von kategorischen Daten in numerische Werte
from tensorflow.keras.models import Sequential  # Zum Erstellen von sequentiellen Modellen in Keras
from tensorflow.keras.layers import Dense, Dropout  # Für die Neuronenschichten und Dropout in Keras
from tensorflow.keras.models import load_model  # Zum Laden von gespeicherten Modellen
from tensorflow.keras.optimizers import Adam  # Der Adam-Optimierer wird zum Trainieren des Modells verwendet
from tensorflow.keras.callbacks import ReduceLROnPlateau  # Zum automatischen Reduzieren der Lernrate

# Pfad zur CSV-Datei, in der die simulierten Spieldaten gespeichert sind
csv_datei = "Simulationen/spieldaten.csv"

# Laden der Daten aus der CSV-Datei mit einer alternativen Codierung
# ISO-8859-1 wird hier verwendet, um sicherzustellen, dass alle Zeichen korrekt gelesen werden
daten = pd.read_csv(csv_datei, encoding='ISO-8859-1')

# Vorbereitung der Eingaben (Features) und Ausgaben (Labels)
# LabelEncoder wird verwendet, um die Karten und den Gewinner in numerische Werte umzuwandeln,
# da maschinelle Lernmodelle nur mit numerischen Daten arbeiten können
label_encoder_karten = LabelEncoder()
label_encoder_gewinner = LabelEncoder()

# Wandeln der Karten in numerische Features um
# Jede Karte wird in eine eindeutige Zahl umgewandelt, die für das Modell als Eingabe verwendet wird
daten['spieler_karte'] = label_encoder_karten.fit_transform(daten['spieler_karte'])
daten['gegner_karte'] = label_encoder_karten.transform(daten['gegner_karte'])
# Der Gewinner des Schlages (Spieler, Gegner oder Unentschieden) wird ebenfalls kodiert
daten['gewinner'] = label_encoder_gewinner.fit_transform(daten['gewinner'])

# Auswahl der Features (Eingaben) und Labels (Zielvariable)
# Die Eingaben (X) bestehen aus den kodierten Karten und den Tokens beider Spieler
X = daten[['spieler_karte', 'gegner_karte', 'spieler_token', 'gegner_token']]
# Die Zielvariable (y) ist der Gewinner des Schlages, den das Modell vorhersagen soll
y = daten['gewinner']

# Aufteilen der Daten in Trainings- und Testdaten
# Die Daten werden in zwei Teile aufgeteilt: 80% zum Trainieren und 20% zum Testen des Modells
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Definition einer Funktion zur Erstellung des Modells
def erstelle_modell():
    # Der Adam-Optimierer wird verwendet, hier mit einer anfänglichen Lernrate von 0.001
    optimizer = Adam(learning_rate=0.001)
    
    # Erstellung eines sequentiellen Modells
    # Ein sequentielles Modell bedeutet, dass die Schichten nacheinander hinzugefügt werden
    modell = Sequential([
        # Erste Schicht: 128 Neuronen, ReLU-Aktivierungsfunktion, Eingabe hat die Dimension der Feature-Anzahl
        Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        # Dropout-Schicht: Verhindert Überanpassung, indem sie zufällig einige Neuronen in dieser Schicht deaktiviert
        Dropout(0.2),
        # Zweite Schicht: 64 Neuronen, ebenfalls mit ReLU aktiviert
        Dense(64, activation='relu'),
        # Ausgabeschicht: 3 Neuronen (eine für jede Klasse: Spieler, Gegner, Unentschieden), Softmax zur Klassifikation
        Dense(3, activation='softmax')
    ])
    
    # Kompilieren des Modells mit dem Optimierer und der Verlustfunktion
    # sparse_categorical_crossentropy ist eine geeignete Verlustfunktion für mehrklassige Klassifikationen mit numerischen Labels
    modell.compile(optimizer=optimizer,
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])
    
    return modell  # Das erstellte Modell wird zurückgegeben

# Überprüfen, ob bereits ein gespeichertes Modell existiert
modell_pfad_neu = "Simulationen/elementar_schlacht_modell.keras"
if os.path.exists(modell_pfad_neu):
    # Wenn das Modell existiert, wird es geladen
    modell = load_model(modell_pfad_neu)
    # Der Optimierer wird erneut konfiguriert, um sicherzustellen, dass die Lernrate stimmt
    optimizer = Adam(learning_rate=0.001)
    modell.compile(optimizer=optimizer,
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])
    print("Modell geladen und wird weitertrainiert.")
else:
    # Wenn kein Modell existiert, wird ein neues Modell erstellt
    modell = erstelle_modell()
    print("Neues Modell erstellt.")

# Callback zur automatischen Reduzierung der Lernrate
# Wenn sich die Validierungsgenauigkeit nach mehreren Epochen nicht verbessert, wird die Lernrate reduziert
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.00001, verbose=1)

# Training des Modells
# Das Modell wird mit den Trainingsdaten trainiert, und es wird eine Validierung mit den Testdaten durchgeführt
# Das Training läuft über 50 Epochen, wobei der ReduceLROnPlateau-Callback verwendet wird
modell.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), callbacks=[reduce_lr])

# Speichern des Modells im neuen Keras-Format (.keras)
modell.save(modell_pfad_neu)
print(f"Modell gespeichert unter: {modell_pfad_neu}")

# Bewertung des Modells auf den Testdaten
# Nach dem Training wird das Modell auf den Testdaten evaluiert, um seine Genauigkeit zu überprüfen
test_loss, test_acc = modell.evaluate(X_test, y_test)
print(f"Testgenauigkeit: {test_acc:.4f}")
