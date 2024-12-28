import csv
import random
from pathlib import Path
import logging
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from scikeras.wrappers import KerasClassifier

# Configure logging
LOG_DATEI = "training.log"
logging.basicConfig(filename=LOG_DATEI, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Define constants
ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft", "Blitz", "Eis", "Magie"]
CSV_DATEI = "Simulationen/spieldaten.csv"
MODELL_PFAD = "Simulationen/elementar_schlacht_modell.keras"
TEST_SIZE = 0.2
RANDOM_STATE = 42
EPOCHS = 10  # Adjusted since hyperparameter optimization is implemented
BATCH_SIZE = 32
HYPERPARAMETER_TUNING = False  # Default is disabled

# Load data
try:
    daten = pd.read_csv(CSV_DATEI, encoding='ISO-8859-1')
    logging.info(f"Daten erfolgreich von {CSV_DATEI} geladen.")
except FileNotFoundError:
    logging.error(f"Fehler: Die Datei {CSV_DATEI} wurde nicht gefunden.")
    print(f"Fehler: Die Datei {CSV_DATEI} wurde nicht gefunden.")
    exit()

# Data preprocessing
def daten_vorverarbeitung(df):
    """
    Preprocesses the data by encoding categorical features and splitting the data into training and testing sets.

    Args:
        df (pd.DataFrame): The raw dataframe containing the game data.

    Returns:
        tuple: A tuple containing the encoded dataframe, labels, and encoders.
    """
    df[['spieler_element', 'spieler_wert']] = df['spieler_karte'].str.split(expand=True)
    df[['gegner_element', 'gegner_wert']] = df['gegner_karte'].str.split(expand=True)

    label_encoder_element = LabelEncoder()
    label_encoder_element.fit(ELEMENTE)
    df['spieler_element'] = label_encoder_element.transform(df['spieler_element'])
    df['gegner_element'] = label_encoder_element.transform(df['gegner_element'])

    label_encoder_wert = LabelEncoder()
    df['spieler_wert'] = label_encoder_wert.fit_transform(df['spieler_wert'])
    df['gegner_wert'] = label_encoder_wert.transform(df['gegner_wert'])

    one_hot_encoder_wetter = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    wetter_encoded = one_hot_encoder_wetter.fit_transform(df[['wetter']])
    wetter_columns = one_hot_encoder_wetter.get_feature_names_out(['wetter'])
    wetter_df = pd.DataFrame(wetter_encoded, columns=wetter_columns)

    one_hot_encoder_held = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    helden_encoded = one_hot_encoder_held.fit_transform(df[['spieler_held', 'gegner_held']])
    helden_columns = one_hot_encoder_held.get_feature_names_out(['spieler_held', 'gegner_held'])
    helden_df = pd.DataFrame(helden_encoded, columns=helden_columns)

    df_encoded = pd.concat([df[['spieler_element', 'spieler_wert', 'spieler_token',
                                   'gegner_element', 'gegner_wert', 'gegner_token']],
                            wetter_df, helden_df], axis=1)

    label_encoder_gewinner = LabelEncoder()
    df['gewinner'] = label_encoder_gewinner.fit_transform(df['gewinner'])

    return df_encoded, df['gewinner'], label_encoder_element, label_encoder_wert, one_hot_encoder_wetter, one_hot_encoder_held, label_encoder_gewinner

daten_encoded, gewinner_labels, le_element, le_wert, ohe_wetter, ohe_held, le_gewinner = daten_vorverarbeitung(daten.copy())

# Split data
X_train, X_test, y_train, y_test = train_test_split(daten_encoded, gewinner_labels, test_size=TEST_SIZE, random_state=RANDOM_STATE)

# Function to create encoding tables
def kodierungs_tabelle_erstellen(le_element, le_wert, ohe_wetter, ohe_held):
    """
    Creates and prints encoding tables for the categorical features.

    Args:
        le_element (LabelEncoder): Label encoder for elements.
        le_wert (LabelEncoder): Label encoder for values.
        ohe_wetter (OneHotEncoder): One-hot encoder for weather.
        ohe_held (OneHotEncoder): One-hot encoder for heroes.
    """
    element_df = pd.DataFrame({'Element': le_element.classes_, 'Kodiert als': le_element.transform(le_element.classes_)})
    wert_df = pd.DataFrame({'Wert': le_wert.classes_, 'Kodiert als': le_wert.transform(le_wert.classes_)})
    wetter_df = pd.DataFrame({'Wetter': ohe_wetter.categories_[0], 'Feature-Spalte': ohe_wetter.get_feature_names_out(['wetter'])})

    # Ensure the input functions are correct
    helden_features = ohe_held.get_feature_names_out(['spieler_held', 'gegner_held'])
    helden_df = pd.DataFrame({'Spieler_Held': ohe_held.categories_[0], 'Feature-Spalte_Spieler': helden_features[:len(ohe_held.categories_[0])]})
    helden_df_gegner = pd.DataFrame({'Gegner_Held': ohe_held.categories_[1], 'Feature-Spalte_Gegner': helden_features[len(ohe_held.categories_[0]):]})

    print("Kodierung der Elemente:\n", element_df)
    print("\nKodierung der Werte:\n", wert_df)
    print("\nOne-Hot-Encoding für Wetter:\n", wetter_df)
    print("\nOne-Hot-Encoding für Helden (Spieler):\n", helden_df)
    print("\nOne-Hot-Encoding für Helden (Gegner):\n", helden_df_gegner)
    logging.info("Kodierungstabellen erstellt und ausgegeben.")

# Call the function to create encoding tables
kodierungs_tabelle_erstellen(le_element, le_wert, ohe_wetter, ohe_held)

# Create model
def erstelle_modell(input_dim, learning_rate=0.001, dropout_rate=0.2, units_dense1=128, units_dense2=64):
    """
    Creates a neural network model.

    Args:
        input_dim (int): The input dimension of the model.
        learning_rate (float): The learning rate for the optimizer.
        dropout_rate (float): The dropout rate for the dropout layers.
        units_dense1 (int): The number of units in the first dense layer.
        units_dense2 (int): The number of units in the second dense layer.

    Returns:
        Sequential: The compiled Keras model.
    """
    optimizer = Adam(learning_rate=learning_rate)
    modell = Sequential([
        Dense(units_dense1, activation='relu', input_shape=(input_dim,)),
        Dropout(dropout_rate),
        Dense(units_dense2, activation='relu'),
        Dense(3, activation='softmax')
    ])
    modell.compile(optimizer=optimizer,
                   loss='sparse_categorical_crossentropy',
                   metrics=['accuracy'])
    return modell

# Model training with optional hyperparameter optimization
def trainiere_modell(modell_pfad, X_train, y_train, X_test, y_test, epochs=EPOCHS, batch_size=BATCH_SIZE):
    """
    Trains the model with optional hyperparameter optimization.

    Args:
        modell_pfad (str): The path to save the model.
        X_train (pd.DataFrame): The training features.
        y_train (pd.Series): The training labels.
        X_test (pd.DataFrame): The testing features.
        y_test (pd.Series): The testing labels.
        epochs (int): The number of epochs for training.
        batch_size (int): The batch size for training.

    Returns:
        Sequential: The trained Keras model.
    """
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=3, min_lr=0.00001, verbose=1)
    callbacks = [early_stopping, reduce_lr]

    if HYPERPARAMETER_TUNING:
        logging.info("Starte Hyperparameter-Optimierung mit GridSearchCV.")
        def create_model_for_tuning(learning_rate, dropout_rate, units_dense1, units_dense2):
            return erstelle_modell(X_train.shape[1], learning_rate=learning_rate, dropout_rate=dropout_rate, units_dense1=units_dense1, units_dense2=units_dense2)

        model_for_tuning = KerasClassifier(model=create_model_for_tuning, verbose=0) # Create the KerasClassifier

        param_grid = {
            'learning_rate': [0.001, 0.0001],
            'dropout_rate': [0.2, 0.3],
            'units_dense1': [128, 256],
            'units_dense2': [64, 128]
        }

        grid = GridSearchCV(estimator=model_for_tuning, param_grid=param_grid, cv=2, scoring='accuracy') # cv=2 for faster demonstration
        grid_result = grid.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, callbacks=callbacks, validation_data=(X_test, y_test))

        print("Beste Hyperparameter:", grid_result.best_params_)
        logging.info(f"Beste Hyperparameter gefunden: {grid_result.best_params_}")
        best_model = grid_result.best_estimator_.model_
    else:
        logging.info("Training des Modells ohne Hyperparameter-Optimierung.")
        if Path(modell_pfad).exists():
            best_model = load_model(modell_pfad)
            logging.info("Modell von der Festplatte geladen und wird weiter trainiert.")
        else:
            best_model = erstelle_modell(X_train.shape[1])
            logging.info("Neues Modell erstellt.")
        history = best_model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batch_size, callbacks=callbacks)
        plot_training_history(history) # Visualization of the training history

    best_model.save(modell_pfad)
    logging.info(f"Modell gespeichert unter: {modell_pfad}")
    return best_model

def plot_training_history(history):
    """
    Plots the training history of the model.

    Args:
        history (History): The training history object returned by the model's fit method.
    """
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Trainingsgenauigkeit')
    plt.plot(history.history['val_accuracy'], label='Validierungsgenauigkeit')
    plt.legend()
    plt.title('Genauigkeit über Epochen')

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Trainingsverlust')
    plt.plot(history.history['val_loss'], label='Validierungsverlust')
    plt.legend()
    plt.title('Verlust über Epochen')
    plt.show()

# Model evaluation
def evaluiere_modell(modell, X_test, y_test):
    """
    Evaluates the model and prints the classification report.

    Args:
        modell (Sequential): The trained Keras model.
        X_test (pd.DataFrame): The testing features.
        y_test (pd.Series): The testing labels.
    """
    test_loss, test_acc = modell.evaluate(X_test, y_test, verbose=0)
    print(f"Testgenauigkeit: {test_acc:.4f}")
    logging.info(f"Testgenauigkeit: {test_acc:.4f}")

    y_pred = np.argmax(modell.predict(X_test), axis=-1)
    print("\nKlassifikationsbericht:")
    print(classification_report(y_test, y_pred))
    logging.info("Klassifikationsbericht erstellt und ausgegeben.")

# Main training loop
if __name__ == "__main__":
    logging.info("Starte den Trainingsprozess.")
    modell = trainiere_modell(MODELL_PFAD, X_train, y_train, X_test, y_test)
    logging.info("Training abgeschlossen.")

    # Model evaluation after training
    logging.info("Starte die Modellevaluation.")
    evaluiere_modell(modell, X_test, y_test)
    logging.info("Modellevaluation abgeschlossen.")
