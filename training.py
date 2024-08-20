import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau

# Pfad zur CSV-Datei
csv_datei = "Simulationen/spieldaten.csv"

# Laden der Daten mit einer alternativen Codierung
daten = pd.read_csv(csv_datei, encoding='ISO-8859-1')

# Vorbereitung der Eingaben (Features) und Ausgaben (Labels)
label_encoder_karten = LabelEncoder()
label_encoder_gewinner = LabelEncoder()

# Wandeln der Karten in Features um
daten['spieler_karte'] = label_encoder_karten.fit_transform(daten['spieler_karte'])
daten['gegner_karte'] = label_encoder_karten.transform(daten['gegner_karte'])
daten['gewinner'] = label_encoder_gewinner.fit_transform(daten['gewinner'])

# Auswahl der Features und Labels
X = daten[['spieler_karte', 'gegner_karte', 'spieler_token', 'gegner_token']]
y = daten['gewinner']

# Aufteilen der Daten in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Beispielhafte Anpassung der Modellstruktur und Hyperparameter
def erstelle_modell():
    optimizer = Adam(learning_rate=0.001)  # Du kannst hier verschiedene Lernraten testen
    
    modell = Sequential([
        Dense(128, activation='relu', input_shape=(X_train.shape[1],)),  # Anzahl der Neuronen erhöht
        Dropout(0.2),  # Dropout hinzugefügt, um Überanpassung zu verhindern
        Dense(64, activation='relu'),  # Weitere versteckte Schicht
        Dense(3, activation='softmax')  # 3 Klassen: Spieler, Gegner, Unentschieden
    ])
    
    modell.compile(optimizer=optimizer,
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])
    return modell

# Überprüfen, ob ein gespeichertes Modell existiert
modell_pfad_neu = "Simulationen/elementar_schlacht_modell.keras"
if os.path.exists(modell_pfad_neu):
    modell = load_model(modell_pfad_neu)
    optimizer = Adam(learning_rate=0.001)
    modell.compile(optimizer=optimizer,
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])
    print("Modell geladen und wird weitertrainiert.")
else:
    modell = erstelle_modell()
    print("Neues Modell erstellt.")

# Lernrate automatisch anpassen, wenn keine Verbesserung auftritt
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.00001, verbose=1)

# Modell trainieren mit dem Callback zur Reduzierung der Lernrate
modell.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), callbacks=[reduce_lr])

# Modell im neuen Keras-Format speichern
modell.save(modell_pfad_neu)
print(f"Modell gespeichert unter: {modell_pfad_neu}")

# Bewertung des Modells auf den Testdaten
test_loss, test_acc = modell.evaluate(X_test, y_test)
print(f"Testgenauigkeit: {test_acc:.4f}")
