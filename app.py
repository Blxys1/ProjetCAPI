import tkinter as tk
from tkinter import ttk, messagebox
from models.players import Player
from models.game import Game

class PlanningPokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Planning Poker")
        self.root.geometry("800x600")

        # Add a style
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12), padding=10)
        self.style.configure("TLabel", font=("Arial", 14))

        self.game = None

        # Initialize Frames
        self.main_menu_frame = tk.Frame(root, bg="#f0f0f0")
        self.setup_frame = tk.Frame(root, bg="#f0f0f0")
        self.voting_frame = tk.Frame(root, bg="#f0f0f0")
        self.results_frame = tk.Frame(root, bg="#f0f0f0")

        # Initialize Main Menu
        self.initialize_main_menu()
        self.switch_frame(self.main_menu_frame)

    def initialize_main_menu(self):
        self.main_menu_frame.pack(fill="both", expand=True)
        tk.Label(self.main_menu_frame, text="Welcome to Planning Poker", font=("Arial", 24, "bold"), bg="#f0f0f0").pack(pady=20)
        ttk.Button(self.main_menu_frame, text="New Game", command=self.new_game).pack(pady=10)
        ttk.Button(self.main_menu_frame, text="Load Game", command=self.load_game).pack(pady=10)
        ttk.Button(self.main_menu_frame, text="Exit", command=self.root.quit).pack(pady=10)

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

        tk.Label(self.setup_frame, text="New Game Setup", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        tk.Label(self.setup_frame, text="Enter Number of Players:", bg="#f0f0f0").pack(pady=10)
        num_players_var = tk.IntVar()
        num_players_entry = ttk.Entry(self.setup_frame, textvariable=num_players_var)
        num_players_entry.pack(pady=5)

        tk.Label(self.setup_frame, text="Enter Rules (strict, average, median, absolute_majority, relative_majority):", bg="#f0f0f0").pack(pady=10)
        rules_var = tk.StringVar()
        rules_entry = ttk.Entry(self.setup_frame, textvariable=rules_var)
        rules_entry.pack(pady=5)

        def setup_players():
            num_players = num_players_var.get()
            rules = rules_var.get()
            if num_players <= 1:
                self.show_popup("Error", "Invalid number of players.")
                return
            if rules not in ["strict", "average", "median", "absolute_majority", "relative_majority"]:
                self.show_popup("Error", "Invalid rules.")
                return

            self.game = Game(num_players=num_players, rules=rules)
            self.collect_player_pseudonyms(num_players)

        ttk.Button(self.setup_frame, text="Next", command=setup_players).pack(pady=20)

    def collect_player_pseudonyms(self, num_players):
        for widget in self.setup_frame.winfo_children():
            widget.destroy()

        tk.Label(self.setup_frame, text="Player Setup", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        self.pseudonym_vars = []
        for i in range(num_players):
            tk.Label(self.setup_frame, text=f"Enter pseudonym for Player {i + 1}:", bg="#f0f0f0").pack(pady=5)
            pseudo_var = tk.StringVar()
            self.pseudonym_vars.append(pseudo_var)
            ttk.Entry(self.setup_frame, textvariable=pseudo_var).pack(pady=5)

        ttk.Button(self.setup_frame, text="Start Game", command=self.start_game).pack(pady=20)

    def start_game(self):
        self.game.players = []
        for pseudo_var in self.pseudonym_vars:
            pseudo = pseudo_var.get()
            if not pseudo:
                self.show_popup("Error", "Pseudonym cannot be empty.")
                return
            self.game.players.append(Player(pseudo))

        self.start_voting()

    def load_game(self):
        try:
            self.game = Game(num_players=0)
            self.game.load_game_state("data/game_state.json")
            self.start_voting()
        except FileNotFoundError:
            self.show_popup("Error", "No saved game found.")
        except Exception as e:
            self.show_popup("Error", f"Error: {str(e)}")

    def start_voting(self):
        self.switch_frame(self.voting_frame)

        for widget in self.voting_frame.winfo_children():
            widget.destroy()

        if not self.game.backlog:
            self.show_popup("Info", "No tasks in backlog to vote on.")
            self.switch_frame(self.main_menu_frame)
            return

        feature = self.game.backlog.pop(0)
        self.game.current_feature = feature

        tk.Label(self.voting_frame, text=f"Current Feature: {feature['description']}", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        self.vote_inputs = {}
        for player in self.game.players:
            frame = tk.Frame(self.voting_frame, bg="#f0f0f0")
            frame.pack(pady=10)
            tk.Label(frame, text=f"{player.pseudo}'s vote: ", font=("Arial", 14), bg="#f0f0f0").pack(side="left")
            var = tk.StringVar()
            self.vote_inputs[player.pseudo] = var
            ttk.Entry(frame, textvariable=var).pack(side="left")

        ttk.Button(self.voting_frame, text="Submit Votes", command=self.submit_votes).pack(pady=20)

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
                self.show_popup("Success", f"Feature '{self.game.current_feature['description']}' validated!")
            else:
                self.show_popup("Info", f"Feature '{self.game.current_feature['description']}' not validated. Revoting...")
                self.game.reset_votes()
                self.start_voting()
                return

            if self.game.backlog:
                self.start_voting()
            else:
                self.display_final_report()
        except Exception as e:
            self.show_popup("Error", f"Error: {str(e)}")

    def display_final_report(self):
        self.switch_frame(self.results_frame)

        tk.Label(self.results_frame, text="Final Report", font=("Arial", 18, "bold"), bg="#f0f0f0").pack(pady=20)

        for feature in self.game.backlog:
            status = "Validated" if feature.get("validated", False) else "Not Validated"
            tk.Label(self.results_frame, text=f"Feature: {feature['description']}, Status: {status}", bg="#f0f0f0").pack(pady=5)

        ttk.Button(self.results_frame, text="Back to Main Menu", command=lambda: self.switch_frame(self.main_menu_frame)).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlanningPokerApp(root)
    root.mainloop()