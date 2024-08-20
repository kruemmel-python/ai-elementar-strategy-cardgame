import os  # Importiert das os-Modul für Betriebssystemoperationen.
import pandas as pd  # Importiert Pandas, um mit Daten in Tabellenform (z.B. CSV-Dateien) zu arbeiten.
import numpy as np  # Importiert NumPy für numerische Operationen.
from sklearn.model_selection import train_test_split  # Importiert die Funktion zum Aufteilen von Daten in Trainings- und Testsets.
from sklearn.preprocessing import LabelEncoder  # Importiert den LabelEncoder, um kategorische Daten in numerische Werte umzuwandeln.
from tensorflow.keras.models import Sequential  # Importiert das Keras-Modul für sequentielle Modellarchitektur.
from tensorflow.keras.layers import Dense, Dropout  # Importiert die Dense- und Dropout-Schichten aus Keras.
from tensorflow.keras.models import load_model  # Importiert die Funktion zum Laden eines Keras-Modells.
from tensorflow.keras.optimizers import Adam  # Importiert den Adam-Optimierer.
from tensorflow.keras.callbacks import ReduceLROnPlateau  # Importiert den Callback zur Reduzierung der Lernrate bei Plateaus.

# Pfad zur CSV-Datei mit den gesammelten Spieldaten
csv_datei = "Simulationen/spieldaten.csv"

# Laden der Daten mit einer alternativen Codierung, um Probleme mit Sonderzeichen zu vermeiden
daten = pd.read_csv(csv_datei, encoding='ISO-8859-1')

# Vorbereitung der Eingaben (Features) und Ausgaben (Labels)
label_encoder_karten = LabelEncoder()  # Initialisiert den LabelEncoder für die Kartendaten.
label_encoder_gewinner = LabelEncoder()  # Initialisiert den LabelEncoder für die Gewinnerdaten.

# Wandelt die Karten in numerische Features um
daten['spieler_karte'] = label_encoder_karten.fit_transform(daten['spieler_karte'])
daten['gegner_karte'] = label_encoder_karten.transform(daten['gegner_karte'])
daten['gewinner'] = label_encoder_gewinner.fit_transform(daten['gewinner'])

# Auswahl der Features und Labels für das Training
X = daten[['spieler_karte', 'gegner_karte', 'spieler_token', 'gegner_token']]  # Die Eingabedaten (Features).
y = daten['gewinner']  # Die Ausgabedaten (Labels).

# Aufteilen der Daten in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def erstelle_modell():
    """
    Erstellt und kompiliert ein Keras-Modell für die Klassifikation.

    Returns:
        Sequential: Das kompilierte Keras-Modell.
    """
    optimizer = Adam(learning_rate=0.001)  # Initialisiert den Adam-Optimierer mit einer Lernrate von 0.001.
    
    modell = Sequential([
        Dense(128, activation='relu', input_shape=(X_train.shape[1],)),  # Erste Schicht mit 128 Neuronen und ReLU-Aktivierungsfunktion.
        Dropout(0.2),  # Dropout-Schicht zur Vermeidung von Überanpassung.
        Dense(64, activation='relu'),  # Zweite Schicht mit 64 Neuronen und ReLU-Aktivierungsfunktion.
        Dense(3, activation='softmax')  # Ausgabeschicht mit Softmax-Aktivierung für 3 Klassen (Spieler, Gegner, Unentschieden).
    ])
    
    modell.compile(optimizer=optimizer,
                   loss='sparse_categorical_crossentropy',  # Verlustfunktion für Mehrklassenklassifikation.
                   metrics=['accuracy'])  # Genauigkeitsmetrik zur Bewertung des Modells.
    return modell  # Gibt das erstellte Modell zurück.

# Überprüfen, ob ein bereits trainiertes Modell existiert
modell_pfad_neu = "Simulationen/elementar_schlacht_modell.keras"
if os.path.exists(modell_pfad_neu):
    modell = load_model(modell_pfad_neu)  # Lädt das vorhandene Modell, wenn es existiert.
    optimizer = Adam(learning_rate=0.001)
    modell.compile(optimizer=optimizer,
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])
    print("Modell geladen und wird weitertrainiert.")
else:
    modell = erstelle_modell()  # Erstellt ein neues Modell, wenn kein vorhandenes Modell gefunden wird.
    print("Neues Modell erstellt.")

# Lernrate automatisch anpassen, wenn keine Verbesserung auftritt
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.00001, verbose=1)

# Modell trainieren mit dem Callback zur Reduzierung der Lernrate
modell.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), callbacks=[reduce_lr])

# Speichern des Modells im Keras-Format
modell.save(modell_pfad_neu)
print(f"Modell gespeichert unter: {modell_pfad_neu}")

# Bewertung des Modells auf den Testdaten
test_loss, test_acc = modell.evaluate(X_test, y_test)
print(f"Testgenauigkeit: {test_acc:.4f}")
