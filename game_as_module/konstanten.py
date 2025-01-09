import os
import random
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np
from tensorflow.keras.models import load_model

# Konstanten und Pfade (Anpassen!)
KARTEN_PFAD = r"G:\ai-elementar-strategy-cardgame-main\PNG\Cards"
ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft", "Blitz", "Eis", "Magie"]
WERTE = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Bube", "Dame", "König", "Ass"]

ELEMENT_HIERARCHIE = {
    "Wasser": {"Feuer": 3, "Erde": 1, "Luft": -3, "Blitz": -3, "Eis": 3},
    "Feuer": {"Erde": 3, "Luft": 1, "Wasser": -3, "Eis": 1, "Blitz": 1},
    "Erde": {"Luft": 3, "Wasser": -1, "Feuer": -3, "Blitz": 3, "Eis": 1},
    "Luft": {"Wasser": 3, "Erde": -1, "Feuer": -3, "Eis": 3, "Blitz": -1},
    "Blitz": {"Wasser": 3, "Erde": 1, "Feuer": 1, "Luft": -3, "Eis": -1},
    "Eis": {"Feuer": 3, "Erde": 1, "Wasser": -3, "Luft": 1, "Blitz": 3},
    "Magie": {"Feuer": 1, "Wasser": 1, "Erde": 1, "Luft": 1, "Blitz": 2, "Eis": 2}
}

HELDEN = {
    "Drache": {"Element": "Feuer", "Bonus": 2},
    "Zauberer": {"Element": "Magie", "Bonus": 3}
}

# Label Encoder for cards
label_encoder_karten = LabelEncoder()
label_encoder_karten.fit(ELEMENTE)

# Hero encoding
label_encoder_held = LabelEncoder()
label_encoder_held.fit(list(HELDEN.keys()))

# One-Hot-Encoder for heroes
one_hot_encoder_held = OneHotEncoder(sparse_output=False)
one_hot_encoder_held.fit(np.array(list(HELDEN.keys())).reshape(-1, 1))

# Weather encoding
label_encoder_wetter = LabelEncoder()
label_encoder_wetter.fit(["Regen", "Windsturm", "Erdbeben"])

# Card value encoding
label_encoder_wert = LabelEncoder()
label_encoder_wert.fit(WERTE)

# Load model
modell_pfad = "Simulationen/elementar_schlacht_modell.keras"
modell = load_model(modell_pfad)
