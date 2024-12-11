import tkinter as tk
from tkinter import messagebox, simpledialog
from models.players import Player
from models.game import Game

class PlanningPokerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Planning Poker")

        self.game = None

        # Main Menu
        self.main_menu_frame = tk.Frame(root)
        self.main_menu_frame.pack(fill="both", expand=True)
        
        tk.Label(self.main_menu_frame, text="Welcome to Planning Poker", font=("Arial", 16)).pack(pady=10)
        tk.Button(self.main_menu_frame, text="New Game", command=self.new_game).pack(pady=5)
        tk.Button(self.main_menu_frame, text="Load Game", command=self.load_game).pack(pady=5)
        tk.Button(self.main_menu_frame, text="Exit", command=root.quit).pack(pady=5)

        # Voting Frame
        self.voting_frame = tk.Frame(root)

    def switch_frame(self, frame):
        for widget in self.root.winfo_children():
            widget.pack_forget()
        frame.pack(fill="both", expand=True)

    def new_game(self):
        num_players = simpledialog.askinteger("New Game", "Enter the number of players:")
        if num_players is None or num_players <= 1:
            messagebox.showerror("Error", "Invalid number of players.")
            return

        rules = simpledialog.askstring("New Game", "Enter rules (strict, average, median, absolute_majority, relative_majority):")
        if rules not in ["strict", "average", "median", "absolute_majority", "relative_majority"]:
            messagebox.showerror("Error", "Invalid rules.")
            return

        self.game = Game(num_players=num_players, rules=rules)

        # Collect pseudonyms via dialog
        self.game.players = []
        for i in range(num_players):
            pseudo = simpledialog.askstring("Player Setup", f"Enter a pseudonym for Player {i + 1}:")
            if not pseudo:
                messagebox.showerror("Error", "Pseudonym cannot be empty.")
                return
            self.game.players.append(Player(pseudo))

        self.start_voting()

    def load_game(self):
        try:
            self.game = Game(num_players=0)
            self.game.load_game_state("data/game_state.json")
            messagebox.showinfo("Load Game", "Game loaded successfully!")
            self.start_voting()
        except FileNotFoundError:
            messagebox.showerror("Error", "No saved game found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def start_voting(self):
        self.switch_frame(self.voting_frame)

        # Clear the frame
        for widget in self.voting_frame.winfo_children():
            widget.destroy()

        if not self.game.backlog:
            messagebox.showinfo("Info", "No tasks in backlog to vote on.")
            self.switch_frame(self.main_menu_frame)
            return

        feature = self.game.backlog.pop(0)
        self.game.current_feature = feature

        tk.Label(self.voting_frame, text=f"Current Feature: {feature['description']}", font=("Arial", 14)).pack(pady=10)

        self.vote_inputs = {}
        for player in self.game.players:
            frame = tk.Frame(self.voting_frame)
            frame.pack(pady=5)
            tk.Label(frame, text=f"{player.pseudo}'s vote: ").pack(side="left")
            var = tk.StringVar()
            self.vote_inputs[player.pseudo] = var
            tk.Entry(frame, textvariable=var).pack(side="left")

        tk.Button(self.voting_frame, text="Submit Votes", command=self.submit_votes).pack(pady=10)

    def submit_votes(self):
        try:
            for player in self.game.players:
                vote = self.vote_inputs[player.pseudo].get()
                player.vote(vote)

            if self.game.process_votes():
                messagebox.showinfo("Feature Validated", f"Feature '{self.game.current_feature['description']}' validated!")
            else:
                messagebox.showinfo("Revote Required", f"Feature '{self.game.current_feature['description']}' not validated. Revoting...")
                self.game.reset_votes()
                self.start_voting()
                return

            if self.game.backlog:
                self.start_voting()
            else:
                messagebox.showinfo("Game Over", "All features validated! Saving final report.")
                self.game.save_final_report()
                self.switch_frame(self.main_menu_frame)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = PlanningPokerApp(root)
    root.mainloop()
