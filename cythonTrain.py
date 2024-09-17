import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau
from dataprocessing import preprocess_data  # Importiere die Cython-optimierte Funktion

# Pfad zur CSV-Datei mit den gesammelten Spieldaten
csv_datei = "Simulationen/spieldaten.csv"

# Laden der Daten
daten = pd.read_csv(csv_datei, encoding='ISO-8859-1')

# Vorbereitung der Eingaben (Features) und Ausgaben (Labels)
X = np.zeros((len(daten), 4), dtype=np.float32)  # Leeres Array für die Datenvorbereitung

# Verwende die Cython-optimierte Funktion
X, y = preprocess_data(X, daten)

# Aufteilen der Daten in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def erstelle_modell():
    optimizer = Adam(learning_rate=0.001)
    
    modell = Sequential([
        Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dense(3, activation='softmax')
    ])
    
    modell.compile(optimizer=optimizer,
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])
    return modell

# Überprüfen, ob ein bereits trainiertes Modell existiert
modell_pfad_neu = "Simulationen/elementar_schlacht_modell.keras"

for i in range(40):  
    if os.path.exists(modell_pfad_neu):
        modell = load_model(modell_pfad_neu)
        optimizer = Adam(learning_rate=0.001)
        modell.compile(optimizer=optimizer,
                       loss='sparse_categorical_crossentropy',
                       metrics=['accuracy'])
        print(f"Modell geladen und wird weitertrainiert. Durchlauf {i+1}")
    else:
        modell = erstelle_modell()
        print(f"Neues Modell erstellt. Durchlauf {i+1}")

    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.00001, verbose=1)
    modell.fit(X_train, y_train, epochs=80, validation_data=(X_test, y_test), callbacks=[reduce_lr])
    modell.save(modell_pfad_neu)
    print(f"Modell gespeichert unter: {modell_pfad_neu} nach Durchlauf {i+1}")

test_loss, test_acc = modell.evaluate(X_test, y_test)
print(f"Testgenauigkeit nach dem zweiten Durchlauf: {test_acc:.4f}")
