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

    def save_game_state(self, filepath="data/game_state.json"):
        """Save the current game state (backlog and player votes) to a file."""
        game_state = {
            "backlog": self.backlog,
            "players": [{"pseudo": player.pseudo, "vote": player.current_vote} for player in self.players]
        }
        with open(filepath, "w") as file:
            json.dump(game_state, file, indent=4)
        print("Game state saved.")


        ### yassmine bsh tzid lhne code mta check for cafe card 


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
            
            # Check the votes and validate the feature
            if self.process_votes():
                feature["validated"] = True
                print(f"Feature '{feature['description']}' validated!")
            else:
                feature["validated"] = False
                print(f"Feature '{feature['description']}' not validated.")
            
            # If all players chose the cafe card, save the state
            if self.check_for_cafe_card():
                break


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
        print("\nVotes collected:")
        
        votes = [player.current_vote for player in self.players]
        print(f"Votes: {votes}")
        
        if self.rules == "strict":
            # Unanimité : Tous les votes doivent être égaux
            if len(set(votes)) == 1:
                print("Unanimity reached! Feature validated.")
            else:
                print("No unanimity. Feature not validated. Revote required.")
                return False
        elif self.rules == "average":
            # Moyenne : Calcul de la moyenne des votes numériques
            valid_votes = [int(vote) for vote in votes if vote != "joker"]
            if valid_votes:
                average = sum(valid_votes) / len(valid_votes)
                print(f"Average vote: {average}")
            else:
                print("No valid votes to calculate an average.")
        elif self.rules == "median":
            # Médiane : Calcul de la médiane
            valid_votes = [int(vote) for vote in votes if vote != "joker"]
            if valid_votes:
                sorted_votes = sorted(valid_votes)
                median = sorted_votes[len(sorted_votes) // 2] if len(sorted_votes) % 2 == 1 else \
                    (sorted_votes[len(sorted_votes) // 2 - 1] + sorted_votes[len(sorted_votes) // 2]) / 2
                print(f"Median vote: {median}")
            else:
                print("No valid votes to calculate a median.")
        else:
            print("No valid rule selected.")
        
        # Réinitialiser les votes pour le prochain tour
        for player in self.players:
            player.reset_vote()
        return True