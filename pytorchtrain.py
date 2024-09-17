import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from torch.utils.data import DataLoader, TensorDataset
print(torch.backends.mps.is_available())  # Für Macs mit M1-Chip
print(torch.cuda.is_available())  # Für NVIDIA GPUs
print(torch.version.hip)  # Für AMD GPUs mit ROCm oder DirectML

# Überprüfen, ob eine GPU verfügbar ist, und das Gerät entsprechend festlegen
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Training auf {device}")

# Pfad zur CSV-Datei mit den gesammelten Spieldaten
csv_datei = "Simulationen/spieldaten.csv"

# Laden der Daten mit einer alternativen Codierung, um Probleme mit Sonderzeichen zu vermeiden
daten = pd.read_csv(csv_datei, encoding='ISO-8859-1')

# Vorbereitung der Eingaben (Features) und Ausgaben (Labels)
label_encoder_karten = LabelEncoder()
label_encoder_gewinner = LabelEncoder()

# Wandelt die Karten in numerische Features um
daten['spieler_karte'] = label_encoder_karten.fit_transform(daten['spieler_karte'])
daten['gegner_karte'] = label_encoder_karten.transform(daten['gegner_karte'])
daten['gewinner'] = label_encoder_gewinner.fit_transform(daten['gewinner'])

# Auswahl der Features und Labels für das Training
X = daten[['spieler_karte', 'gegner_karte', 'spieler_token', 'gegner_token']].values
y = daten['gewinner'].values

# Aufteilen der Daten in Trainings- und Testdaten
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Konvertiere die Daten in PyTorch-Tensoren
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.long)
X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
y_test_tensor = torch.tensor(y_test, dtype=torch.long)

# Erstellen von DataLoadern für das Training und Testing
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

# Definition des Modells
class KartenModel(nn.Module):
    def __init__(self):
        super(KartenModel, self).__init__()
        self.fc1 = nn.Linear(4, 128)
        self.dropout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, 3)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x

# Initialisiere das Modell, die Verlustfunktion und den Optimierer
model = KartenModel().to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Trainingsschleife
def train_model(num_epochs=80):
    model.train()  # Setzt das Modell in den Trainingsmodus
    for epoch in range(num_epochs):
        running_loss = 0.0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            optimizer.zero_grad()  # Zurücksetzen der Gradienten
            
            outputs = model(inputs)  # Vorwärtsdurchlauf
            loss = criterion(outputs, labels)  # Verlust berechnen
            loss.backward()  # Rückwärtsdurchlauf
            optimizer.step()  # Optimierer-Schritt
            
            running_loss += loss.item()
        
        print(f"Epoch [{epoch+1}/{num_epochs}], Verlust: {running_loss/len(train_loader):.4f}")

# Trainingsphase starten
train_model()

# Modell evaluieren
def evaluate_model():
    model.eval()  # Setzt das Modell in den Evaluierungsmodus
    correct = 0
    total = 0
    with torch.no_grad():  # Deaktiviert das Berechnen der Gradienten für schnelleres Testen
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    print(f"Testgenauigkeit: {100 * correct / total:.2f}%")

# Bewertung des Modells
evaluate_model()
