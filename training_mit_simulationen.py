import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau

# Alle möglichen Elemente, die vorkommen können
ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft", "Blitz", "Eis", "Magie"]

# Pfad zur CSV-Datei mit den gesammelten Spieldaten
csv_datei = "Simulationen/spieldaten.csv"

# Laden der Daten
daten = pd.read_csv(csv_datei, encoding='ISO-8859-1')

# Aufteilen der Kartenspalten in Element und Wert
daten['spieler_element'] = daten['spieler_karte'].apply(lambda x: x.split()[0])
daten['spieler_wert'] = daten['spieler_karte'].apply(lambda x: x.split()[1])

daten['gegner_element'] = daten['gegner_karte'].apply(lambda x: x.split()[0])
daten['gegner_wert'] = daten['gegner_karte'].apply(lambda x: x.split()[1])

# LabelEncoder für Kartenelemente mit allen möglichen Elementen trainieren
label_encoder_element = LabelEncoder()
label_encoder_element.fit(ELEMENTE)  # Trainiere den Encoder mit allen möglichen Elementen

# Kodierung der Elemente (sowohl für Spieler als auch für Gegner)
daten['spieler_element'] = label_encoder_element.transform(daten['spieler_element'])
daten['gegner_element'] = label_encoder_element.transform(daten['gegner_element'])

# Kodierung der Kartenwerte (analog für Kartenwerte)
label_encoder_wert = LabelEncoder()
daten['spieler_wert'] = label_encoder_wert.fit_transform(daten['spieler_wert'])
daten['gegner_wert'] = label_encoder_wert.transform(daten['gegner_wert'])

# One-Hot-Encoding für das Wetter
one_hot_encoder_wetter = OneHotEncoder()
wetter_encoded = one_hot_encoder_wetter.fit_transform(daten[['wetter']]).toarray()
wetter_columns = one_hot_encoder_wetter.get_feature_names_out(['wetter'])

# One-Hot-Encoding für Helden: Kombiniere Spielerheld und Gegnerheld
one_hot_encoder_held = OneHotEncoder()
helden_encoded = one_hot_encoder_held.fit_transform(daten[['spieler_held', 'gegner_held']]).toarray()
helden_columns = one_hot_encoder_held.get_feature_names_out(['spieler_held', 'gegner_held'])

# Erstellen eines DataFrames mit den One-Hot-encoded Daten
wetter_df = pd.DataFrame(wetter_encoded, columns=wetter_columns)
helden_df = pd.DataFrame(helden_encoded, columns=helden_columns)

# Verbinden der Daten in einen neuen DataFrame
daten_encoded = pd.concat([daten[['spieler_element', 'spieler_wert', 'spieler_token', 
                                  'gegner_element', 'gegner_wert', 'gegner_token']],
                           wetter_df, helden_df], axis=1)

# Label für das Training (Gewinner)
label_encoder_gewinner = LabelEncoder()
daten['gewinner'] = label_encoder_gewinner.fit_transform(daten['gewinner'])

# Auswahl der Features (Eingabedaten) und Labels (Ausgabedaten)
X = daten_encoded  # Alle Features aus den One-Hot-Encoding-Prozessen
y = daten['gewinner']  # Labels sind der Gewinner des Spiels

# Aufteilen der Daten in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Ausgabe der Kodierungen für Label-Encoder und One-Hot-Encoder
def kodierungs_tabelle_erstellen():
    # Erstellen der Tabellen für Element- und Wert-Kodierungen
    element_df = pd.DataFrame({
        'Element': label_encoder_element.classes_,
        'Kodiert als': range(len(label_encoder_element.classes_))
    })

    wert_df = pd.DataFrame({
        'Wert': label_encoder_wert.classes_,
        'Kodiert als': range(len(label_encoder_wert.classes_))
    })

    # Erstellen der Tabelle für Wetter und Helden (One-Hot-Kodierungen)
    wetter_df = pd.DataFrame({
        'Wetter': one_hot_encoder_wetter.categories_[0],
        'Feature-Spalte': wetter_columns
    })

    helden_df = pd.DataFrame({
        'Spieler_und_Gegner_Helden': np.concatenate(one_hot_encoder_held.categories_),
        'Feature-Spalte': helden_columns
    })

    # Ausgabe der Tabellen
    print("Kodierung der Elemente:")
    print(element_df)
    print("\nKodierung der Werte:")
    print(wert_df)
    print("\nOne-Hot-Encoding für Wetter:")
    print(wetter_df)
    print("\nOne-Hot-Encoding für Helden:")
    print(helden_df)

# Aufrufen der Funktion, um die Kodierungstabellen zu drucken
kodierungs_tabelle_erstellen()

# Rest des Trainingscodes (Modellerstellung und Training)
def erstelle_modell(input_dim):
    optimizer = Adam(learning_rate=0.001)

    modell = Sequential([
        Dense(128, activation='relu', input_shape=(input_dim,)),
        Dropout(0.2),
        Dense(64, activation='relu'),
        Dense(3, activation='softmax')  # Drei Klassen: Spieler gewinnt, Gegner gewinnt, Unentschieden
    ])

    modell.compile(optimizer=optimizer,
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])
    return modell

# Überprüfen, ob ein bereits trainiertes Modell existiert
modell_pfad_neu = "Simulationen/elementar_schlacht_modell.keras"

for i in range(3):  # Schleife, um das Training mehrfach durchzuführen
    if os.path.exists(modell_pfad_neu):
        modell = load_model(modell_pfad_neu)
        optimizer = Adam(learning_rate=0.001)
        modell.compile(optimizer=optimizer,
                       loss='sparse_categorical_crossentropy',
                       metrics=['accuracy'])
        print(f"Modell geladen und wird weitertrainiert. Durchlauf {i+1}")
    else:
        modell = erstelle_modell(X_train.shape[1])  # Erstellt ein neues Modell, wenn kein vorhandenes Modell gefunden wird.
        print(f"Neues Modell erstellt. Durchlauf {i+1}")

    # Lernrate automatisch anpassen, wenn keine Verbesserung auftritt
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.00001, verbose=1)

    # Modell trainieren mit dem Callback zur Reduzierung der Lernrate
    modell.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), callbacks=[reduce_lr])

    # Speichern des Modells im Keras-Format
    modell.save(modell_pfad_neu)
    print(f"Modell gespeichert unter: {modell_pfad_neu} nach Durchlauf {i+1}")

# Bewertung des Modells auf den Testdaten
test_loss, test_acc = modell.evaluate(X_test, y_test)
print(f"Testgenauigkeit nach dem zweiten Durchlauf: {test_acc:.4f}")
