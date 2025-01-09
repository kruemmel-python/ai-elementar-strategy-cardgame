import os
import random
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np
from tensorflow.keras.models import load_model

# Konstanten und Pfade (Anpassen!)
# Hier werden die Pfade und Konstanten für das Spiel definiert.
KARTEN_PFAD = r"G:\ai-elementar-strategy-cardgame-main\PNG\Cards" # Pfad zu den Kartenbildern
ELEMENTE = ["Feuer", "Wasser", "Erde", "Luft", "Blitz", "Eis", "Magie"] # Liste aller Kartenelemente
WERTE = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Bube", "Dame", "König", "Ass"] # Liste aller Kartenwerte

# Die Elementhierarchie definiert, wie stark ein Element gegen ein anderes ist.
# Positive Werte bedeuten einen Vorteil, negative Werte einen Nachteil und 0 bedeutet neutral.
ELEMENT_HIERARCHIE = {
    "Wasser": {"Feuer": 3, "Erde": 1, "Luft": -3, "Blitz": -3, "Eis": 3},
    "Feuer": {"Erde": 3, "Luft": 1, "Wasser": -3, "Eis": 1, "Blitz": 1},
    "Erde": {"Luft": 3, "Wasser": -1, "Feuer": -3, "Blitz": 3, "Eis": 1},
    "Luft": {"Wasser": 3, "Erde": -1, "Feuer": -3, "Eis": 3, "Blitz": -1},
    "Blitz": {"Wasser": 3, "Erde": 1, "Feuer": 1, "Luft": -3, "Eis": -1},
    "Eis": {"Feuer": 3, "Erde": 1, "Wasser": -3, "Luft": 1, "Blitz": 3},
    "Magie": {"Feuer": 1, "Wasser": 1, "Erde": 1, "Luft": 1, "Blitz": 2, "Eis": 2}
}

# Helden haben spezifische Elemente und Boni.
HELDEN = {
    "Drache": {"Element": "Feuer", "Bonus": 2},
    "Zauberer": {"Element": "Magie", "Bonus": 3}
}

# Label Encoder für Karten
# Ein Label Encoder wandelt Kategorien (z.B. "Feuer", "Wasser") in numerische Werte um.
# Das ist notwendig, damit maschinelle Lernmodelle damit arbeiten können.
label_encoder_karten = LabelEncoder()
# Der Label Encoder lernt hier alle vorhandenen Elemente kennen.
label_encoder_karten.fit(ELEMENTE)

# Heldenkodierung
# Hier wird ein Label Encoder für die Helden vorbereitet.
label_encoder_held = LabelEncoder()
# Der Encoder lernt alle Heldnamen.
label_encoder_held.fit(list(HELDEN.keys()))

# One-Hot-Encoder für Helden
# Ein One-Hot-Encoder wandelt Kategorien in Vektoren um, wobei jedes Element
# eine eigene Dimension hat und nur eine Dimension mit 1 markiert ist.
# Das ist nützlich, um Kategorien für neuronale Netze darzustellen.
one_hot_encoder_held = OneHotEncoder(sparse_output=False)
# Der One-Hot Encoder lernt, wie die Helden zu codieren sind.
one_hot_encoder_held.fit(np.array(list(HELDEN.keys())).reshape(-1, 1))

# Wetterkodierung
# Hier wird der Label Encoder für das Wetter vorbereitet.
label_encoder_wetter = LabelEncoder()
# Der Encoder lernt alle Wetterbedingungen.
label_encoder_wetter.fit(["Regen", "Windsturm", "Erdbeben"])

# Kartenwertkodierung
# Der Label Encoder für die Kartenwerte.
label_encoder_wert = LabelEncoder()
# Der Encoder lernt alle Kartenwerte.
label_encoder_wert.fit(WERTE)

# Modell laden
# Hier wird das trainierte neuronale Netzwerk geladen.
modell_pfad = "Simulationen/elementar_schlacht_modell.keras"
# Das Modell wird aus der Datei geladen.
modell = load_model(modell_pfad)
