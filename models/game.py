import json
from models.players import Player

class Game:
    def __init__(self, num_players, rules="strict"):
        self.players = []
        self.backlog = []
        self.rules = rules  # "strict", "average", "median", etc.
        self.current_feature = None
        self.load_backlog("data/backlog.json")
        self.initialize_players(num_players)

    def initialize_players(self, num_players):
        """Initialize players and collect their pseudonyms."""
        for i in range(num_players):
            pseudo = input(f"Enter a pseudonym for Player {i+1}: ")
            self.players.append(Player(pseudo))
        print(f"{num_players} players have been added.")

    def load_backlog(self, filepath):
        """Loads backlog items from a JSON file."""
        try:
            with open(filepath, "r") as file:
                self.backlog = json.load(file).get("tasks", [])
            print("Backlog loaded successfully.")
        except FileNotFoundError:
            print("Backlog file not found. Starting with an empty backlog.")
            self.backlog = []

    def start_game(self):
        """Main loop for running the game, where each player votes on each feature."""
        # Ensure there is a backlog to process
        if not self.backlog:
            print("No tasks in backlog to vote on.")
            return
        
        # Loop through each feature in the backlog
        for feature in self.backlog:
            self.current_feature = feature
            print(f"\nCurrent feature: {feature['description']}")
            
            # Collect votes from each player for the current feature
            self.collect_votes()
            
            # Placeholder: Here you would check votes based on the rules
            self.process_votes() # Implement voting logic based on rules here

    def collect_votes(self):
        """Collects votes from each player for the current feature."""
        for player in self.players:
            while True:
                print(f"{player.pseudo}, available cards: {', '.join(player.cards)}")
                card = input(f"{player.pseudo}, choose a card: ")
                try:
                    player.vote(card)
                    break  # Exit the loop if the vote is valid
                except ValueError as e:
                    print(e)  # Ask for input again if card is invalid

def process_votes(self):
        """Process the votes based on the chosen rules."""
        # For now, print each player's vote as a placeholder
        print("\nVotes collected:")
        for player in self.players:
            print(f"{player.pseudo}'s vote: {player.current_vote}")
        
        # Reset each player's vote for the next round
        for player in self.players:
            player.reset_vote()