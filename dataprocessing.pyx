# -*- coding: utf-8 -*-
import numpy as np
cimport numpy as np
from sklearn.preprocessing import LabelEncoder
import pandas as pd

# Definition der Funktion zur Vorverarbeitung
def preprocess_data(np.ndarray[np.float32_t, ndim=2] X, object daten):
    # LabelEncoder sind Python-Objekte, deshalb nutzen wir hier kein 'cdef'
    label_encoder_karten = LabelEncoder()
    label_encoder_gewinner = LabelEncoder()

    # Numerische Transformation der Kartendaten
    daten['spieler_karte'] = label_encoder_karten.fit_transform(daten['spieler_karte'])
    daten['gegner_karte'] = label_encoder_karten.transform(daten['gegner_karte'])
    daten['gewinner'] = label_encoder_gewinner.fit_transform(daten['gewinner'])

    # Umwandeln in numpy float32 Arrays
    X[:] = daten[['spieler_karte', 'gegner_karte', 'spieler_token', 'gegner_token']].values.astype(np.float32)
    y = daten['gewinner'].values.astype(np.int32)
    
    return X, y
