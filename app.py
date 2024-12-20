import tkinter as tk
from tkinter import ttk, messagebox
from models.players import Player
from models.game import Game
import os


class PlanningPokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Planning Poker")
        self.root.geometry("800x600")

        # Ensure the save directory exists
        os.makedirs("data", exist_ok=True)

        # Style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 16), padding=15)
        self.style.configure("TLabel", font=("Arial", 20))

        self.game = None

        # Frames
        self.main_menu_frame = tk.Frame(root, bg="#8699c2")
        self.setup_frame = tk.Frame(root, bg="#8699c2")
        self.voting_frame = tk.Frame(root, bg="#8699c2")
        self.results_frame = tk.Frame(root, bg="#8699c2")

        # Main menu
        self.initialize_main_menu()
        self.switch_frame(self.main_menu_frame)
    

    def initialize_main_menu(self):
        self.main_menu_frame.pack(fill="both", expand=True)
        tk.Label(self.main_menu_frame, text="Bienvenue à Poker Planning", font=("Arial", 30, "bold"), bg="#a81125").pack(pady=20)
        ttk.Button(self.main_menu_frame, text="Nouvelle Partie", command=self.new_game).pack(pady=15)
        ttk.Button(self.main_menu_frame, text="Charger Partie", command=self.load_game).pack(pady=15)
        ttk.Button(self.main_menu_frame, text="Quitter", command=self.root.quit).pack(pady=15)

    def switch_frame(self, frame):
        for widget in self.root.winfo_children():
            widget.pack_forget()
        frame.pack(fill="both", expand=True)

    def show_popup(self, title, message):
        messagebox.showinfo(title, message)

    def new_game(self):
        self.switch_frame(self.setup_frame)
        self.initialize_setup_frame()

    def initialize_setup_frame(self):
        for widget in self.setup_frame.winfo_children():
            widget.destroy()

        tk.Label(self.setup_frame, text="Nouveau Jeu", font=("Arial", 20, "bold"), bg="#a81125").pack(pady=20)

        tk.Label(self.setup_frame, text="Enter Nombre De Joueurs ( Attention Supérieur à 1 ! )",  font=("Arial", 12), bg="#456499").pack(pady=20)
        num_players_var = tk.IntVar()
        ttk.Entry(self.setup_frame, textvariable=num_players_var).pack(pady=10)

        tk.Label(self.setup_frame, text="Choisir Règles (strict, average, median, absolute_majority, relative_majority):", font=("Arial", 12), bg="#456499").pack(pady=20)
        rules_var = tk.StringVar()
        ttk.Entry(self.setup_frame, textvariable=rules_var).pack(pady=20)

        def setup_players():
            num_players = num_players_var.get()
            rules = rules_var.get()
            if num_players <= 1:
                self.show_popup("Error", "Nombre Invalide! Entrez un nombre valid.")
                return
            if rules not in ["strict", "average", "median", "absolute_majority", "relative_majority"]:
                self.show_popup("Error", "Règle Invalide! Entrer une règle valide.")
                return

            self.game = Game(num_players=num_players, rules=rules)
            self.collect_player_pseudonyms(num_players)

        ttk.Button(self.setup_frame, text="Suivant", command=setup_players).pack(pady=20)

    def collect_player_pseudonyms(self, num_players):
        for widget in self.setup_frame.winfo_children():
            widget.destroy()

        tk.Label(self.setup_frame, text="Choix Joueur", font=("Arial", 20, "bold"), bg="#a81125").pack(pady=20)

        self.pseudonym_vars = []
        for i in range(num_players):
            tk.Label(self.setup_frame, text=f"Enter pseudonym pour Joueur numero {i + 1}:", font=("Arial", 12),  bg="#456499").pack(pady=10)
            pseudo_var = tk.StringVar()
            self.pseudonym_vars.append(pseudo_var)
            ttk.Entry(self.setup_frame, textvariable=pseudo_var).pack(pady=10)

        ttk.Button(self.setup_frame, text="Commencer le Jeu", command=self.start_game).pack(pady=20)

    def start_game(self):
        self.game.players = []
        for pseudo_var in self.pseudonym_vars:
            pseudo = pseudo_var.get()
            if not pseudo:
                self.show_popup("Error", "Pseudonym ne peut pas être vide.")
                return
            self.game.players.append(Player(pseudo))

        self.start_voting()

    def load_game(self):
        try:
            self.game = Game(num_players=0)
            self.game.load_game_state("data/game_state.json")
            self.start_voting()
        except FileNotFoundError:
            self.show_popup("Error", "Aucune sauvegarde trouvée.")
        except Exception as e:
            self.show_popup("Error", f"Error: {str(e)}")

    def start_voting(self):
        self.switch_frame(self.voting_frame)
        for widget in self.voting_frame.winfo_children():
            widget.destroy()

        if not self.game.current_feature:
            self.game.current_feature = self.game.backlog[0]

        current_feature = self.game.current_feature
        tk.Label(self.voting_frame, text=f"Tache actuelle : {current_feature['description']}", 
                 font=("Arial", 18, "bold"), bg="#456499").pack(pady=20)

        self.vote_inputs = {}
        for player in self.game.players:
            frame = tk.Frame(self.voting_frame, bg="#456499")
            frame.pack(pady=10)
            tk.Label(frame, text=f"Le vote de {player.pseudo}: ", bg="#f0f0f0").pack(side="left")
            tk.Label(frame, text=f"Carte Disponible: {', '.join(player.cards)}",  bg="#f0f0f0").pack(pady=5)
            var = tk.StringVar()
            self.vote_inputs[player.pseudo] = var
            ttk.Entry(frame, textvariable=var).pack(side="left")

        ttk.Button(self.voting_frame, text="Valider Vote", command=self.submit_votes).pack(pady=30)

    def submit_votes(self):
        try:
            for player in self.game.players:
                vote = self.vote_inputs[player.pseudo].get()
                try:
                    player.vote(vote)
                except ValueError as e:
                    self.show_popup("Error", str(e))
                    return

            if self.game.process_votes():
                self.show_popup("Succès", f"Tache Actuelle:  '{self.game.current_feature['description']}' validée!")
                
                # Move to the next feature without removing from backlog
                current_index = self.game.backlog.index(self.game.current_feature)
                self.game.backlog[current_index]["validated"] = True

                # Check if there are more tasks
                if any(not task.get("validated", False) for task in self.game.backlog):
                    # Find the next unvalidated feature
                    for feature in self.game.backlog:
                        if not feature.get("validated", False):
                            self.game.current_feature = feature
                            break
                    self.start_voting()
                else:
                    # All tasks are validated, save the final report
                    self.game.save_final_report("data/final_report.json")
                    self.display_final_report()
            else:
                self.show_popup("Info", f"Tache Actuelle: '{self.game.current_feature['description']}' non validé. Veuillez refaire le vote...")
                self.game.reset_votes()
                self.start_voting()
        except Exception as e:
            self.show_popup("Error", f"Error: {str(e)}")

    def display_final_report(self):
        self.switch_frame(self.results_frame)

        tk.Label(self.results_frame, text=" Rapport Final", font=("Arial", 20, "bold"), bg="#a81125").pack(pady=30)

        for feature in self.game.backlog:
            status = "Validated" if feature.get("validated", False) else "Not Validated"
            tk.Label(self.results_frame, text=f"Tache Actuelle: {feature['description']}, Status: {status}", font=("Arial", 16) , bg="#f0f0f0").pack(pady=10)

        ttk.Button(self.results_frame, text="Retour Menu Principal", command=lambda: self.switch_frame(self.main_menu_frame)).pack(pady=20)


if __name__ == "__main__":
    root = tk.Tk()
    app = PlanningPokerApp(root)
    root.mainloop()
