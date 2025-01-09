import os
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from spiel import Spiel
from konstanten import KARTEN_PFAD, HELDEN, WERTE

class GrafikInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Elementar Schlacht")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.attributes('-fullscreen', True)  # Vollbildmodus entfernt
        self.resizable(True, True)  # Allow resizing
        self.spiel = None
        self.karten_bilder = self.lade_kartenbilder()
        self.karte_labels = []
        self.spieler_karte_label = None
        self.gegner_karte_label = None
        self.spieler_token_var = tk.StringVar()
        self.gegner_token_var = tk.StringVar()
        self.spieler_token_label = None
        self.gegner_token_label = None
        self.auswertung_text = None
        self.neustart_button = None
        self.beenden_button = None
        
        # Style for themed look
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Define colors
        self.background_color = '#f0f0f0'
        self.button_color = '#d0d0d0'
        self.text_color = '#333333'
        self.highlight_color = '#add8e6'
        self.config(bg=self.background_color)

        self.initialisiere_gui()
        self.starte_neues_spiel()

    def lade_kartenbilder(self):
        """Loads card images."""
        karten_bilder = {}
        for filename in os.listdir(KARTEN_PFAD):
            if filename.lower().endswith(".png"):
                try:
                    image = Image.open(os.path.join(KARTEN_PFAD, filename))
                    image = image.resize((150, 225), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    karten_bilder[filename.replace(".png", "")] = photo
                except Exception as e:
                     print(f"Fehler beim Laden des Bildes {filename}: {e}")
        return karten_bilder
    
    def initialisiere_gui(self):
         """Initializes the GUI."""

         # Main frame for layout
         main_frame = ttk.Frame(self, padding="10", style="Main.TFrame")
         main_frame.pack(fill="both", expand=True)

         # Left frame for card display
         left_frame = ttk.Frame(main_frame, style="Card.TFrame")
         left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

         # Player Info (under the text box)
         self.spieler_info_frame = ttk.Frame(main_frame, padding="10", style="Info.TFrame")
         self.spieler_info_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

         ttk.Label(self.spieler_info_frame, text="Dein Held: ", style="Info.TLabel").grid(row=0, column=0, padx=10) # Text wird später angepasst

         self.spieler_token_label = ttk.Label(self.spieler_info_frame, textvariable=self.spieler_token_var, style="Token.TLabel")
         self.spieler_token_label.grid(row=0, column=1, padx=10)


         # AI Cards
         ai_card_frame = ttk.Frame(left_frame, style="AiCard.TFrame")
         ai_card_frame.pack(side="top", padx=10, pady=10, fill="x", expand=True)

         self.gegner_token_label = ttk.Label(ai_card_frame, textvariable=self.gegner_token_var, style="Token.TLabel")
         self.gegner_token_label.pack(pady=5)

         ttk.Label(ai_card_frame, text="KI's Hand", style="AiCard.TLabel").pack(pady=5)

         self.ai_cards_frame = ttk.Frame(ai_card_frame, style="Card.TFrame")
         self.ai_cards_frame.pack(pady=5)


         # Player cards
         player_card_frame = ttk.Frame(left_frame, style="PlayerCard.TFrame")
         player_card_frame.pack(side="bottom", padx=10, pady=10, fill="x", expand=True)

         ttk.Label(player_card_frame, text="Deine Hand", style="PlayerCard.TLabel").pack(pady=5)

         self.karten_frame = ttk.Frame(player_card_frame, style="Card.TFrame")
         self.karten_frame.pack(pady=5)

         # Played card display (player and ai)
         self.played_cards_frame = ttk.Frame(main_frame, style="PlayedCards.TFrame")
         self.played_cards_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

         self.gegner_karte_label = ttk.Label(self.played_cards_frame, text="KI Karte", style="AiCard.TLabel")
         self.gegner_karte_label.pack(side="top", padx=10, pady=10)

         self.spieler_karte_label = ttk.Label(self.played_cards_frame, text="Spieler Karte", style="PlayerCard.TLabel")
         self.spieler_karte_label.pack(side="bottom", padx=10, pady=10)


         # Evaluation/Status area
         self.auswertung_frame = ttk.Frame(main_frame, padding="10", style="Status.TFrame")
         self.auswertung_frame.grid(row=0, column=2, sticky="nsew", padx=10, pady=10, rowspan=2)  # Make it fill vertically
         self.auswertung_frame.rowconfigure(0, weight=1) # Allow the Text area to expand
         self.auswertung_text = tk.Text(self.auswertung_frame,  wrap="word", font=("Arial", 10))  # Smaller text area
         self.auswertung_text.pack(fill="both", expand=True) # Fill all the space available
         self.auswertung_text.config(state="disabled")

        # Style configuration
         self.style.configure("Main.TFrame", background=self.background_color)
         self.style.configure("Info.TFrame", background=self.background_color)
         self.style.configure("Card.TFrame", background=self.background_color)
         self.style.configure("PlayerCard.TFrame", background=self.background_color, borderwidth=2, relief="groove")
         self.style.configure("AiCard.TFrame", background=self.background_color, borderwidth=2, relief="groove")
         self.style.configure("PlayedCards.TFrame", background=self.background_color, borderwidth=2, relief="groove")
         self.style.configure("Status.TFrame", background=self.background_color)
         self.style.configure("Token.TLabel", background=self.background_color, font=("Arial", 12))
         self.style.configure("PlayerCard.TLabel", background=self.background_color, font=("Arial", 12))
         self.style.configure("AiCard.TLabel", background=self.background_color, font=("Arial", 12))
         self.style.configure("TButton", background=self.button_color, foreground=self.text_color, font=("Arial", 12))

         # Make the grid responsive
         main_frame.columnconfigure(1, weight=1)
         main_frame.columnconfigure(2, weight=1)
         main_frame.rowconfigure(0, weight=1)
         main_frame.rowconfigure(1, weight=0)
         left_frame.rowconfigure(0, weight=1)
         left_frame.rowconfigure(1, weight=1)
    
    def starte_neues_spiel(self):
        """Startet ein neues Spiel."""
        self.spiel = Spiel()
        self.spieler_token_var.set(str(self.spiel.spieler_token))
        self.gegner_token_var.set(str(self.spiel.gegner_token))
        # Aktualisieren des Helden-Labels
        self.spieler_info_frame.winfo_children()[0].config(text=f"Dein Held: {self.spiel.held} ({HELDEN[self.spiel.held]['Bonus']} Bonus auf {HELDEN[self.spiel.held]['Element']})")
        self.update_karten_anzeige()
        self.update_gegner_karten_anzeige()
        self.zeige_status()

    def update_karten_anzeige(self):
        """Updates the display of player's cards."""
        # Löschen der alten Buttons
        for button in self.karte_labels:
            button.destroy()
        self.karte_labels = []  # Zurücksetzen der Liste

        for i, (element, wert) in enumerate(self.spiel.spieler_hand):
            # Adjust the card name generation to handle "König" correctly
            if wert == "König":
                karten_name = f"card_{element.lower()}_koenig"
            else:
               karten_name = f"card_{element.lower()}_{wert.lower()}"

            if karten_name not in self.karten_bilder:
                karten_name = "card_back"

            card_image = self.karten_bilder.get(karten_name)
            if card_image:
                card_button = tk.Button(self.karten_frame, image=card_image, command=lambda index=i: self.karte_auswaehlen(index), borderwidth=0, highlightbackground=self.highlight_color, relief="solid")
                card_button.image = card_image  # Referenz speichern
                card_button.pack(side="left", padx=5, pady=5)
                self.karte_labels.append(card_button)
            else:
                print(f"Kein Bild für Karte {karten_name} gefunden.")

    def update_gegner_karten_anzeige(self):
            """Updates the display of opponent's cards."""
            # Clear old labels in ai_cards_frame
            for widget in self.ai_cards_frame.winfo_children():
                widget.destroy()

            # Show only the back of the cards for the AI
            card_image = self.karten_bilder.get("card_back")
            if card_image:
                for _ in range(len(self.spiel.gegner_hand)):
                    card_label = tk.Label(self.ai_cards_frame, image=card_image, borderwidth=0)
                    card_label.image = card_image  # keep a reference to the image
                    card_label.pack(side="left", padx=5, pady=5)
            else:
                print(f"Kein Bild für Karte card_back gefunden.")

    def karte_auswaehlen(self, karten_index):
        """Handles card selection by the player."""
        if self.spiel.karte_waehlen(karten_index):
            self.update_karten_anzeige()
            self.update_gegner_karten_anzeige()
            self.zeige_status()
        else:
            messagebox.showerror("Fehler", "Ungültige Kartenauswahl.")

    def zeige_status(self):
        """Updates the GUI status."""
        self.spieler_token_var.set(str(self.spiel.spieler_token))
        self.gegner_token_var.set(str(self.spiel.gegner_token))

        if self.spiel.wettereffekt:
            wettertext = f"Wettereffekt: {self.spiel.wettereffekt}"
        else:
            wettertext = "Kein Wettereffekt."

        if self.spiel.gegner_karte:
             gegner_karte_text = f"KI spielt: {self.spiel.gegner_karte[0]} {self.spiel.gegner_karte[1]}"
             # Adjust the card name generation to handle "König" correctly
             if self.spiel.gegner_karte[1] == "König":
                 gegner_karten_name = f"card_{self.spiel.gegner_karte[0].lower()}_koenig"
             else:
                 gegner_karten_name = f"card_{self.spiel.gegner_karte[0].lower()}_{self.spiel.gegner_karte[1].lower()}"

             if gegner_karten_name not in self.karten_bilder:
                 gegner_karten_name = "card_back"
             
             card_image = self.karten_bilder.get(gegner_karten_name)
             if card_image:
                 if self.gegner_karte_label.winfo_children():
                     self.gegner_karte_label.winfo_children()[0].destroy()
                 card_label = tk.Label(self.gegner_karte_label, image=card_image)
                 card_label.image = card_image
                 card_label.pack()
        else:
             gegner_karte_text = "KI hat noch keine Karte gespielt"
             if self.gegner_karte_label.winfo_children():
                    self.gegner_karte_label.winfo_children()[0].destroy()


        if self.spiel.spieler_karte:
            spieler_karte_text = f"Du spielst: {self.spiel.spieler_karte[0]} {self.spiel.spieler_karte[1]}"
            
            # Adjust the card name generation to handle "König" correctly
            if self.spiel.spieler_karte[1] == "König":
               spieler_karten_name = f"card_{self.spiel.spieler_karte[0].lower()}_koenig"
            else:
                spieler_karten_name = f"card_{self.spiel.spieler_karte[0].lower()}_{self.spiel.spieler_karte[1].lower()}"

            if spieler_karten_name not in self.karten_bilder:
                spieler_karten_name = "card_back"

            card_image = self.karten_bilder.get(spieler_karten_name)
            if card_image:
                if self.spieler_karte_label.winfo_children():
                    self.spieler_karte_label.winfo_children()[0].destroy()
                card_label = tk.Label(self.spieler_karte_label, image=card_image)
                card_label.image = card_image
                card_label.pack()

        else:
           spieler_karte_text = "Du hast noch keine Karte gespielt"
           if self.spieler_karte_label.winfo_children():
                    self.spieler_karte_label.winfo_children()[0].destroy()


        auswertung_text = ""
        if self.spiel.gewinner is not None:
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
        """

           if self.spiel.gewinner == "spieler":
               gewinner_text = f"Der Gewinner des Schlages ist: Spieler"
           elif self.spiel.gewinner == "gegner":
               gewinner_text = f"Der Gewinner des Schlages ist: KI"
           else:
              gewinner_text = f"Der Schlag endet unentschieden."
           auswertung_text = auswertung_text + gewinner_text

        if self.spiel.spiel_ende():
            auswertung_text = auswertung_text + self.spiel.get_gewinner_text()
            self.zeige_spielende_fenster(self.spiel.get_gewinner_text())

        self.auswertung_text.config(state="normal")  # Textfeld aktivieren
        self.auswertung_text.delete("1.0", tk.END)  # Inhalt löschen
        self.auswertung_text.insert(tk.END, wettertext + "\n\n" + spieler_karte_text + "\n\n" + gegner_karte_text + "\n\n" + auswertung_text)
        self.auswertung_text.config(state="disabled") # Textfeld deaktivieren

    def zeige_spielende_fenster(self, text):
        """Zeigt ein Fenster am Spielende mit Neustart/Beenden Optionen."""
        top = tk.Toplevel(self)
        top.title("Spielende")
        top.geometry("300x150")

        message_label = ttk.Label(top, text=text, padding=10)
        message_label.pack()
        
        button_frame = ttk.Frame(top)
        button_frame.pack(pady=10)
        
        self.neustart_button = ttk.Button(button_frame, text="Neustart", command=lambda: [top.destroy(), self.starte_neues_spiel()])
        self.neustart_button.pack(side="left", padx=10)
        
        self.beenden_button = ttk.Button(button_frame, text="Beenden", command=self.on_closing)
        self.beenden_button.pack(side="left", padx=10)


    def on_closing(self):
        """Wird ausgeführt, wenn das Fenster geschlossen wird."""
        if messagebox.askokcancel("Beenden", "Möchten Sie das Spiel wirklich beenden?"):
            self.destroy()

if __name__ == "__main__":
    app = GrafikInterface()
    app.mainloop()