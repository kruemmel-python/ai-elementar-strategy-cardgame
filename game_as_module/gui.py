import os  # Importiert das 'os'-Modul, das Funktionen zur Interaktion mit dem Betriebssystem bereitstellt (z.B. zum Auflisten von Dateien in einem Verzeichnis).
import tkinter as tk  # Importiert das Tkinter-Modul unter dem Alias 'tk' für die Erstellung der grafischen Benutzeroberfläche.
from tkinter import ttk, messagebox  # Importiert spezifische Tkinter-Module: ttk für thematisierte Widgets und messagebox für Dialogfenster.
from PIL import Image, ImageTk  # Importiert Module aus der Pillow-Bibliothek (PIL) zur Bildverarbeitung.
from spiel import Spiel  # Importiert die Klasse 'Spiel' aus der Datei 'spiel.py' (vermutlich Spiellogik).
from konstanten import KARTEN_PFAD, HELDEN, WERTE  # Importiert Konstanten aus der Datei 'konstanten.py' (z.B. Dateipfade und Spielwerte).

class GrafikInterface(tk.Tk):
    """
    Eine Klasse, die das grafische Interface für das Elementar-Schlacht-Spiel erstellt.
    Sie erbt von tk.Tk, was sie zum Hauptfenster der Anwendung macht.
    """
    def __init__(self):
        """
        Initialisiert das Hauptfenster des Spiels.
        Setzt den Titel, konfiguriert das Schließen des Fensters,
        lädt Kartenbilder, initialisiert GUI-Elemente und startet ein neues Spiel.
        """
        super().__init__()  # Ruft den Konstruktor der Elternklasse tk.Tk auf, um das Hauptfenster zu initialisieren.
        self.title("Elementar Schlacht")  # Setzt den Titel des Fensters.
        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # Verknüpft das Schließen des Fensters mit der Methode 'on_closing'.
        # self.attributes('-fullscreen', True)  # Vollbildmodus entfernt (auskommentiert)
        self.resizable(True, True)  # Erlaubt die Größenänderung des Fensters in horizontaler und vertikaler Richtung.
        self.spiel = None  # Initialisiert das 'spiel'-Attribut mit 'None', wird später eine Instanz der 'Spiel'-Klasse speichern.
        self.karten_bilder = self.lade_kartenbilder()  # Lädt die Bilder für die Spielkarten.
        self.karte_labels = []  # Eine Liste, die Labels für die Karten des Spielers speichert.
        self.spieler_karte_label = None # Label, welches die vom Spieler gespielte Karte anzeigt
        self.gegner_karte_label = None # Label, welches die von der KI gespielte Karte anzeigt
        self.spieler_token_var = tk.StringVar()  # Tkinter Variable für die Anzahl der Token des Spielers
        self.gegner_token_var = tk.StringVar()  # Tkinter Variable für die Anzahl der Token des Gegners (KI)
        self.spieler_token_label = None # Label, das die Anzahl der Token des Spielers anzeigt
        self.gegner_token_label = None # Label, das die Anzahl der Token des Gegners (KI) anzeigt
        self.auswertung_text = None # Text-Widget zur Anzeige von Spielinformationen und Ergebnissen
        self.neustart_button = None # Button zum Neustarten des Spiels
        self.beenden_button = None # Button zum Beenden des Spiels
        
        # Style for themed look
        self.style = ttk.Style(self) # Erstellt einen Style um das Aussehen der Widgets anzupassen
        self.style.theme_use('clam') # Setzt das Theme auf "clam", ein modernes und flaches Design
    
        # Define colors
        self.background_color = '#f0f0f0'  # Definiert die Hintergrundfarbe für die GUI
        self.button_color = '#d0d0d0'     # Definiert die Farbe für Buttons
        self.text_color = '#333333'       # Definiert die Textfarbe
        self.highlight_color = '#add8e6'  # Definiert die Farbe, um ausgewählte Karten zu highlighten
        self.config(bg=self.background_color) # Setzt die Hintergrundfarbe des Hauptfensters
    
        self.initialisiere_gui()  # Initialisiert alle GUI-Elemente.
        self.starte_neues_spiel()  # Startet ein neues Spiel.

    def lade_kartenbilder(self):
        """
        Lädt alle Kartenbilder aus dem KARTEN_PFAD.
        Gibt ein Dictionary zurück, das die Bilddateinamen mit den PhotoImage-Objekten verknüpft.
        """
        karten_bilder = {}  # Initialisiert ein Dictionary, um die geladenen Bilder zu speichern.
        for filename in os.listdir(KARTEN_PFAD):  # Iteriert über alle Dateien im Verzeichnis KARTEN_PFAD.
            if filename.lower().endswith(".png"):  # Überprüft, ob die Datei eine PNG-Datei ist (Groß-/Kleinschreibung wird ignoriert).
                try:
                    image = Image.open(os.path.join(KARTEN_PFAD, filename))  # Öffnet das Bild mit Pillow.
                    image = image.resize((150, 225), Image.Resampling.LANCZOS)  # Passt die Bildgröße an und verwendet LANCZOS für eine hohe Qualität
                    photo = ImageTk.PhotoImage(image)  # Konvertiert das Pillow-Bild in ein Tkinter-kompatibles PhotoImage.
                    karten_bilder[filename.replace(".png", "")] = photo  # Speichert das PhotoImage im Dictionary mit dem Dateinamen (ohne .png) als Schlüssel.
                except Exception as e:
                     print(f"Fehler beim Laden des Bildes {filename}: {e}") # Gibt Fehlermeldungen aus, falls ein Bild nicht geladen werden kann
        return karten_bilder  # Gibt das Dictionary mit den geladenen Bildern zurück.
    
    def initialisiere_gui(self):
         """
         Initialisiert die grafische Benutzeroberfläche (GUI).
         Erstellt verschiedene Frames und Labels zur Anzeige von Karten, Token und Spielstatus.
         """
         # Main frame for layout
         main_frame = ttk.Frame(self, padding="10", style="Main.TFrame") # Erstellt einen Hauptframe mit Padding und zugewiesenem Style
         main_frame.pack(fill="both", expand=True)  # Packt den Frame so, dass er sich ausfüllt und expandiert

         # Left frame for card display
         left_frame = ttk.Frame(main_frame, style="Card.TFrame") # Erstellt einen Frame für die Kartenanzeige mit zugewiesenem Style
         left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10) # Platziert den Frame im Grid, füllt ihn und fügt Padding hinzu

         # Player Info (under the text box)
         self.spieler_info_frame = ttk.Frame(main_frame, padding="10", style="Info.TFrame") # Frame, der die Spielerinformationen enthält mit zugewiesenem Style
         self.spieler_info_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10) # Platziert den Frame im Grid, spannt über 3 Spalten und füllt die Zeile aus

         ttk.Label(self.spieler_info_frame, text="Dein Held: ", style="Info.TLabel").grid(row=0, column=0, padx=10) # Erstellt ein Label, um den Helden anzuzeigen

         self.spieler_token_label = ttk.Label(self.spieler_info_frame, textvariable=self.spieler_token_var, style="Token.TLabel")  # Label zur Anzeige der Spieler-Token, Text wird über eine Variable aktualisiert
         self.spieler_token_label.grid(row=0, column=1, padx=10)  # Platziert das Token-Label im Grid

         # AI Cards
         ai_card_frame = ttk.Frame(left_frame, style="AiCard.TFrame") # Frame für die Anzeige der KI-Karten mit zugewiesenem Style
         ai_card_frame.pack(side="top", padx=10, pady=10, fill="x", expand=True) # Packt den Frame so, dass er sich ausfüllt und expandiert

         self.gegner_token_label = ttk.Label(ai_card_frame, textvariable=self.gegner_token_var, style="Token.TLabel") # Label zur Anzeige der KI-Token, Text wird über eine Variable aktualisiert
         self.gegner_token_label.pack(pady=5) # Fügt das Token Label mit Padding hinzu

         ttk.Label(ai_card_frame, text="KI's Hand", style="AiCard.TLabel").pack(pady=5) # Label für den KI Hand Bereich

         self.ai_cards_frame = ttk.Frame(ai_card_frame, style="Card.TFrame") # Frame, in dem die KI-Karten angezeigt werden, mit zugewiesenem Style
         self.ai_cards_frame.pack(pady=5) # Packt den Frame mit Padding

         # Player cards
         player_card_frame = ttk.Frame(left_frame, style="PlayerCard.TFrame")  # Frame für die Anzeige der Spieler-Karten mit zugewiesenem Style
         player_card_frame.pack(side="bottom", padx=10, pady=10, fill="x", expand=True)  # Packt den Frame so, dass er sich ausfüllt und expandiert

         ttk.Label(player_card_frame, text="Deine Hand", style="PlayerCard.TLabel").pack(pady=5) # Label für den Spieler Hand Bereich

         self.karten_frame = ttk.Frame(player_card_frame, style="Card.TFrame") # Frame für die Karten des Spielers
         self.karten_frame.pack(pady=5)  # Packt den Frame mit Padding

         # Played card display (player and ai)
         self.played_cards_frame = ttk.Frame(main_frame, style="PlayedCards.TFrame") # Frame für die Anzeige der gespielten Karten
         self.played_cards_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)  # Platziert den Frame im Grid, füllt ihn und fügt Padding hinzu

         self.gegner_karte_label = ttk.Label(self.played_cards_frame, text="KI Karte", style="AiCard.TLabel") # Label, das die gespielte Karte der KI anzeigt
         self.gegner_karte_label.pack(side="top", padx=10, pady=10) # Positioniert das Label mit Padding

         self.spieler_karte_label = ttk.Label(self.played_cards_frame, text="Spieler Karte", style="PlayerCard.TLabel") # Label, das die gespielte Karte des Spielers anzeigt
         self.spieler_karte_label.pack(side="bottom", padx=10, pady=10) # Positioniert das Label mit Padding

         # Evaluation/Status area
         self.auswertung_frame = ttk.Frame(main_frame, padding="10", style="Status.TFrame")  # Frame, der die Auswertung des Spiels anzeigt
         self.auswertung_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10, rowspan=2)  # Platziert den Frame im Grid, füllt ihn und fügt Padding hinzu, rowspan sorgt dafür das es 2 Zeilen einnimmt
         self.auswertung_frame.rowconfigure(0, weight=1)  # Sorgt dafür das der Text-Bereich expandiert
         self.auswertung_text = tk.Text(self.auswertung_frame,  wrap="word", font=("Arial", 10))  # Text-Widget zur Anzeige von Status und Ergebnissen, wrap sorgt für den Zeilenumbruch und es wird die Schriftart Arial mit der Größe 10 genutzt
         self.auswertung_text.pack(fill="both", expand=True)  # Packt das Text-Widget so, dass es sich ausfüllt und expandiert
         self.auswertung_text.config(state="disabled") # Setzt den Text-Bereich auf nicht bearbeitbar

        # Style configuration
         self.style.configure("Main.TFrame", background=self.background_color)   # Konfiguriert die Hintergrundfarbe für den Hauptframe
         self.style.configure("Info.TFrame", background=self.background_color)   # Konfiguriert die Hintergrundfarbe für den Info-Frame
         self.style.configure("Card.TFrame", background=self.background_color)   # Konfiguriert die Hintergrundfarbe für den Kartenframe
         self.style.configure("PlayerCard.TFrame", background=self.background_color, borderwidth=2, relief="groove")  # Konfiguriert den Spieler-Kartenframe mit Rahmen
         self.style.configure("AiCard.TFrame", background=self.background_color, borderwidth=2, relief="groove")      # Konfiguriert den KI-Kartenframe mit Rahmen
         self.style.configure("PlayedCards.TFrame", background=self.background_color, borderwidth=2, relief="groove") # Konfiguriert den Frame der gespielten Karten mit Rahmen
         self.style.configure("Status.TFrame", background=self.background_color) # Konfiguriert den Statusframe
         self.style.configure("Token.TLabel", background=self.background_color, font=("Arial", 12))   # Konfiguriert das Token-Label mit Hintergrundfarbe und Schriftart
         self.style.configure("PlayerCard.TLabel", background=self.background_color, font=("Arial", 12)) # Konfiguriert das Spieler-Karten-Label mit Hintergrundfarbe und Schriftart
         self.style.configure("AiCard.TLabel", background=self.background_color, font=("Arial", 12))   # Konfiguriert das KI-Karten-Label mit Hintergrundfarbe und Schriftart
         self.style.configure("TButton", background=self.button_color, foreground=self.text_color, font=("Arial", 12)) # Konfiguriert das Aussehen der Buttons

         # Make the grid responsive
         main_frame.columnconfigure(1, weight=1)  # Erlaubt Spalte 1 sich auszudehnen wenn das Fenster größer wird
         main_frame.columnconfigure(2, weight=1)  # Erlaubt Spalte 2 sich auszudehnen wenn das Fenster größer wird
         main_frame.rowconfigure(0, weight=1) # Erlaubt Zeile 0 sich auszudehnen wenn das Fenster größer wird
         main_frame.rowconfigure(1, weight=0) # Erlaubt Zeile 1 sich nicht auszudehnen
         left_frame.rowconfigure(0, weight=1)  # Erlaubt Zeile 0 des linken Frames sich auszudehnen
         left_frame.rowconfigure(1, weight=1)  # Erlaubt Zeile 1 des linken Frames sich auszudehnen
    
    def starte_neues_spiel(self):
        """
        Startet ein neues Spiel.
        Initialisiert das Spielobjekt, setzt Token und aktualisiert die GUI.
        """
        self.spiel = Spiel()  # Erstellt ein neues Spielobjekt.
        self.spieler_token_var.set(str(self.spiel.spieler_token))  # Aktualisiert die Tkinter Variable mit der Anzahl der Spieler-Token
        self.gegner_token_var.set(str(self.spiel.gegner_token))  # Aktualisiert die Tkinter Variable mit der Anzahl der KI-Token
        # Aktualisieren des Helden-Labels
        self.spieler_info_frame.winfo_children()[0].config(text=f"Dein Held: {self.spiel.held} ({HELDEN[self.spiel.held]['Bonus']} Bonus auf {HELDEN[self.spiel.held]['Element']})") # Aktualisiert das Heldenlabel mit dem Held und dem entsprechenden Bonus
        self.update_karten_anzeige()  # Aktualisiert die Anzeige der Karten des Spielers.
        self.update_gegner_karten_anzeige() # Aktualisiert die Anzeige der Karten des Gegners.
        self.zeige_status()  # Aktualisiert die Statusanzeige.

    def update_karten_anzeige(self):
        """
        Aktualisiert die Anzeige der Karten des Spielers.
        Löscht alte Karten-Buttons und erstellt neue für die aktuelle Hand des Spielers.
        """
        # Löschen der alten Buttons
        for button in self.karte_labels:  # Iteriert über alle vorhandenen Karten-Buttons
            button.destroy()  # Entfernt den Button aus der GUI
        self.karte_labels = []  # Setzt die Liste der Karten-Buttons zurück

        for i, (element, wert) in enumerate(self.spiel.spieler_hand):  # Iteriert über die Karten in der Spielerhand.
            # Adjust the card name generation to handle "König" correctly
            if wert == "König": # Falls die Karte ein König ist, wird "koenig" an den Kartennamen angehangen
                karten_name = f"card_{element.lower()}_koenig" # Generiert den Dateinamen für das Kartenbild
            else:
               karten_name = f"card_{element.lower()}_{wert.lower()}" # Generiert den Dateinamen für das Kartenbild

            if karten_name not in self.karten_bilder:  # Überprüft ob ein Bild zu der Karte existiert
                karten_name = "card_back" # Wenn nicht, dann wird das Standardbild "card_back" geladen

            card_image = self.karten_bilder.get(karten_name)  # Holt das Bild aus dem Dictionary der geladenen Bilder.
            if card_image:  # Überprüft, ob ein Bild gefunden wurde
                card_button = tk.Button(self.karten_frame, image=card_image, command=lambda index=i: self.karte_auswaehlen(index), borderwidth=0, highlightbackground=self.highlight_color, relief="solid")  # Erstellt einen Button mit dem Kartenbild und einem Command, um die Karte auszuwählen.
                card_button.image = card_image  # Referenz speichern (wichtig, damit das Bild nicht vom Garbage Collector entfernt wird)
                card_button.pack(side="left", padx=5, pady=5)  # Packt den Button in den Frame mit Padding
                self.karte_labels.append(card_button)  # Fügt den Button zur Liste der Karten-Buttons hinzu
            else:
                print(f"Kein Bild für Karte {karten_name} gefunden.")  # Gibt eine Fehlermeldung aus, falls kein Bild gefunden wurde

    def update_gegner_karten_anzeige(self):
            """
            Aktualisiert die Anzeige der Karten des Gegners (KI).
            Löscht alte Karten-Labels und zeigt für jede Karte der KI-Hand die Rückseite der Karte an.
            """
            # Clear old labels in ai_cards_frame
            for widget in self.ai_cards_frame.winfo_children(): # Iteriert über alle Widgets im Frame der KI Karten
                widget.destroy() # Löscht jedes Widget

            # Show only the back of the cards for the AI
            card_image = self.karten_bilder.get("card_back") # Holt das Bild der Kartenrückseite
            if card_image: # Überprüft, ob ein Bild gefunden wurde
                for _ in range(len(self.spiel.gegner_hand)): # Iteriert über die Anzahl der Karten in der KI Hand
                    card_label = tk.Label(self.ai_cards_frame, image=card_image, borderwidth=0) # Erstellt ein Label, um die Kartenrückseite anzuzeigen
                    card_label.image = card_image  # keep a reference to the image (wichtig, damit das Bild nicht vom Garbage Collector entfernt wird)
                    card_label.pack(side="left", padx=5, pady=5)  # Packt die Karte in den Frame mit Padding
            else:
                print(f"Kein Bild für Karte card_back gefunden.")  # Gibt eine Fehlermeldung aus, falls kein Bild gefunden wurde

    def karte_auswaehlen(self, karten_index):
        """
        Behandelt die Auswahl einer Karte durch den Spieler.
        Ruft die entsprechende Methode des Spielobjekts auf und aktualisiert die GUI.
        """
        if self.spiel.karte_waehlen(karten_index):  # Versucht die Karte im Spiel zu wählen
            self.update_karten_anzeige()  # Aktualisiert die Anzeige der Karten des Spielers.
            self.update_gegner_karten_anzeige() # Aktualisiert die Anzeige der Karten des Gegners.
            self.zeige_status()  # Aktualisiert die Statusanzeige.
        else:
            messagebox.showerror("Fehler", "Ungültige Kartenauswahl.")  # Zeigt eine Fehlermeldung an, wenn die Kartenauswahl ungültig war.

    def zeige_status(self):
        """
        Aktualisiert die Statusanzeige der GUI.
        Zeigt die Anzahl der Token, Wettereffekte, gespielte Karten und die Auswertung des Schlags.
        """
        self.spieler_token_var.set(str(self.spiel.spieler_token))  # Aktualisiert die Anzeige der Token des Spielers.
        self.gegner_token_var.set(str(self.spiel.gegner_token))  # Aktualisiert die Anzeige der Token des Gegners.

        if self.spiel.wettereffekt: # Überprüft ob ein Wettereffekt aktiv ist
            wettertext = f"Wettereffekt: {self.spiel.wettereffekt}"  # Formatiert den Text für den Wettereffekt
        else:
            wettertext = "Kein Wettereffekt."  # Setzt den Text, wenn kein Wettereffekt aktiv ist.

        if self.spiel.gegner_karte: # Überprüft, ob der Gegner eine Karte gespielt hat
             gegner_karte_text = f"KI spielt: {self.spiel.gegner_karte[0]} {self.spiel.gegner_karte[1]}" # Formatiert den Text für die gespielte Karte der KI
             # Adjust the card name generation to handle "König" correctly
             if self.spiel.gegner_karte[1] == "König": # Überprüft ob die KI einen König gespielt hat
                 gegner_karten_name = f"card_{self.spiel.gegner_karte[0].lower()}_koenig" # Generiert den Dateinamen für die Karte
             else:
                 gegner_karten_name = f"card_{self.spiel.gegner_karte[0].lower()}_{self.spiel.gegner_karte[1].lower()}" # Generiert den Dateinamen für die Karte

             if gegner_karten_name not in self.karten_bilder: # Überprüft ob die Karte ein Bild hat
                 gegner_karten_name = "card_back" # Wenn nicht, wird die Kartenrückseite verwendet
             
             card_image = self.karten_bilder.get(gegner_karten_name) # Holt das Bild der Karte
             if card_image: # Überprüft ob ein Bild existiert
                 if self.gegner_karte_label.winfo_children(): # Überprüft ob das Label schon ein Kind-Widget (ein Bild) hat
                     self.gegner_karte_label.winfo_children()[0].destroy()  # Löscht das Kind-Widget (das alte Bild)
                 card_label = tk.Label(self.gegner_karte_label, image=card_image) # Erstellt ein neues Label mit dem Bild der Karte
                 card_label.image = card_image # Behält eine Referenz zum Bild
                 card_label.pack() # Fügt das Label zum Frame hinzu
        else:
             gegner_karte_text = "KI hat noch keine Karte gespielt" # Falls die KI keine Karte gespielt hat
             if self.gegner_karte_label.winfo_children(): # Überprüft ob das Label schon ein Kind-Widget (ein Bild) hat
                    self.gegner_karte_label.winfo_children()[0].destroy() # Löscht das Kind-Widget (das alte Bild)

        if self.spiel.spieler_karte: # Überprüft, ob der Spieler eine Karte gespielt hat
            spieler_karte_text = f"Du spielst: {self.spiel.spieler_karte[0]} {self.spiel.spieler_karte[1]}" # Formatiert den Text der Spielerkarte
            
            # Adjust the card name generation to handle "König" correctly
            if self.spiel.spieler_karte[1] == "König": # Überprüft ob der Spieler einen König gespielt hat
               spieler_karten_name = f"card_{self.spiel.spieler_karte[0].lower()}_koenig" # Generiert den Dateinamen für die Karte
            else:
                spieler_karten_name = f"card_{self.spiel.spieler_karte[0].lower()}_{self.spiel.spieler_karte[1].lower()}"  # Generiert den Dateinamen für die Karte

            if spieler_karten_name not in self.karten_bilder:  # Überprüft, ob das Bild der Karte vorhanden ist
                spieler_karten_name = "card_back"  # Falls nicht, wird das Standardbild verwendet

            card_image = self.karten_bilder.get(spieler_karten_name) # Holt das Bild der Karte
            if card_image: # Überprüft ob ein Bild vorhanden ist
                if self.spieler_karte_label.winfo_children(): # Überprüft ob das Label schon ein Kind-Widget (ein Bild) hat
                    self.spieler_karte_label.winfo_children()[0].destroy() # Löscht das Kind-Widget (das alte Bild)
                card_label = tk.Label(self.spieler_karte_label, image=card_image) # Erstellt ein neues Label mit dem Bild der Karte
                card_label.image = card_image  # Behält eine Referenz zum Bild
                card_label.pack() # Fügt das Label zum Frame hinzu

        else:
           spieler_karte_text = "Du hast noch keine Karte gespielt"  # Setzt den Text, falls der Spieler noch keine Karte gespielt hat
           if self.spieler_karte_label.winfo_children():  # Überprüft ob das Label schon ein Kind-Widget (ein Bild) hat
                    self.spieler_karte_label.winfo_children()[0].destroy()  # Löscht das Kind-Widget (das alte Bild)

        auswertung_text = "" # Setzt die Variable für den Auswertungstext auf leer
        if self.spiel.gewinner is not None: # Überprüft, ob ein Gewinner existiert
           auswertung_text = f"""
        **********************************************************************************************************************************************
        Auswertung:
        {spieler_karte_text}
        Spieler Kartenwert = {WERTE.index(self.spiel.spieler_karte[1])} (Index von {self.spiel.spieler_karte[1]} in der Liste WERTE)
        Spieler Elementbonus = {self.spiel.spieler_elementbonus}
        Spieler Heldenbonus = {self.spiel.spieler_heldenbonus}
        Spieler hat {self.spiel.spieler_token} Tokens → Tokenbonus = {self.spiel.spieler_bonus}
        Gesamtwert Spieler = {WERTE.index(self.spiel.spieler_karte[1])} (Kartenwert) + {self.spiel.spieler_elementbonus} (Elementbonus) + {self.spiel.spieler_heldenbonus} (Heldenbonus) + {self.spiel.spieler_bonus} (Tokenbonus) = {self.spiel.spieler_gesamtwert}

        {gegner_karte_text}
        KI Kartenwert = {WERTE.index(self.spiel.gegner_karte[1])} (Index von {self.spiel.gegner_karte[1]} in der Liste WERTE)
        KI Elementbonus = {self.spiel.gegner_elementbonus}
        KI Heldenbonus = {self.spiel.gegner_heldenbonus}
        KI hat {self.spiel.gegner_token} Tokens → Tokenbonus = {self.spiel.gegner_bonus}
        Gesamtwert KI = {WERTE.index(self.spiel.gegner_karte[1])} (Kartenwert) + {self.spiel.gegner_elementbonus} (Elementbonus) + {self.spiel.gegner_heldenbonus} (Heldenbonus) + {self.spiel.gegner_bonus} (Tokenbonus) = {self.spiel.gegner_gesamtwert}
        ************************************************************************************************************************************************
        """ # Formatiert den Text für die Auswertung

           if self.spiel.gewinner == "spieler": # Überprüft, wer den Schlag gewonnen hat
               gewinner_text = f"Der Gewinner des Schlages ist: Spieler" # Formatiert den Text für den Gewinner
           elif self.spiel.gewinner == "gegner": # Überprüft, wer den Schlag gewonnen hat
               gewinner_text = f"Der Gewinner des Schlages ist: KI" # Formatiert den Text für den Gewinner
           else:
              gewinner_text = f"Der Schlag endet unentschieden."  # Formatiert den Text falls es Unentschieden ist
           auswertung_text = auswertung_text + gewinner_text # Fügt den Gewinner Text zum Auswertungstext hinzu

        if self.spiel.spiel_ende():  # Überprüft, ob das Spielende erreicht wurde
            auswertung_text = auswertung_text + self.spiel.get_gewinner_text() # Fügt den Text zum Ende des Spiels zum Auswertungstext hinzu
            self.zeige_spielende_fenster(self.spiel.get_gewinner_text()) # Zeigt ein Fenster mit dem Ergebnis des Spiels an

        self.auswertung_text.config(state="normal")  # Aktiviert das Text-Widget, um Text einzufügen
        self.auswertung_text.delete("1.0", tk.END)  # Löscht den aktuellen Inhalt des Text-Widgets
        self.auswertung_text.insert(tk.END, wettertext + "\n\n" + spieler_karte_text + "\n\n" + gegner_karte_text + "\n\n" + auswertung_text) # Fügt den formatierten Text ein
        self.auswertung_text.config(state="disabled")  # Deaktiviert das Text-Widget, um es nicht bearbeitbar zu machen

    def zeige_spielende_fenster(self, text):
        """
        Zeigt ein Fenster am Spielende mit Neustart/Beenden Optionen.
        Erstellt ein neues Toplevel-Fenster mit einer Meldung und Buttons.
        """
        top = tk.Toplevel(self)  # Erstellt ein neues Toplevel-Fenster.
        top.title("Spielende")  # Setzt den Titel des neuen Fensters
        top.geometry("300x150") # Setzt die Größe des Fensters
    
        message_label = ttk.Label(top, text=text, padding=10)  # Erstellt ein Label, um den Text anzuzeigen.
        message_label.pack() # Packt das Label in das Fenster
        
        button_frame = ttk.Frame(top) # Erstellt ein Frame für die Buttons
        button_frame.pack(pady=10) # Packt den Frame mit Padding
        
        self.neustart_button = ttk.Button(button_frame, text="Neustart", command=lambda: [top.destroy(), self.starte_neues_spiel()])  # Erstellt einen Button zum Neustarten des Spiels
        self.neustart_button.pack(side="left", padx=10) # Packt den Button mit Padding
        
        self.beenden_button = ttk.Button(button_frame, text="Beenden", command=self.on_closing) # Erstellt einen Button zum Beenden des Spiels
        self.beenden_button.pack(side="left", padx=10) # Packt den Button mit Padding


    def on_closing(self):
        """
        Wird aufgerufen, wenn das Hauptfenster geschlossen wird.
        Fragt den Benutzer, ob er das Spiel wirklich beenden möchte.
        """
        if messagebox.askokcancel("Beenden", "Möchten Sie das Spiel wirklich beenden?"):  # Zeigt eine Bestätigungsbox
            self.destroy()  # Schließt das Hauptfenster

if __name__ == "__main__":
    app = GrafikInterface()  # Erstellt eine Instanz der 'GrafikInterface'-Klasse.
    app.mainloop()  # Startet die Tkinter-Ereignisschleife, die die GUI anzeigt und auf Benutzereingaben reagiert.
