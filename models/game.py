import json
from models.players import Player
import os


class Game:
    """
    @class Game
    @brief Represents the Planning Poker game and its rules.


    """
    
    #def timeout(pseudo, timeout_duration=10):
     #   """Notify the player if they run out of time to vote."""
      #  print(f"{pseudo}, you have {timeout_duration} seconds to vote.")
       # threading.Timer(timeout_duration, lambda: print(f"Time is up for {pseudo}!")).start()

    def __init__(self, num_players, rules="strict"):
        """@brief Constructor for the Game class.
        @param num_players The number of players in the game.
        @param rules The voting rules to use for the game   


            """
        self.players = []
        self.backlog = []
        self.rules = rules  # "strict", "average", "median", etc.
        self.current_feature = None
        # Ensure the save directory exists
        os.makedirs("data", exist_ok=True)

        # Auto-create save file
        if not os.path.exists("data/game_state.json"):
            self.save_game_state()
        self.load_backlog("data/backlog.json")
        self.initialize_players(num_players)

    def initialize_players(self, num_players):

        """@brief Initialize players and collect their pseudonyms.
        @param num_players The number of players to initialize.
            
            """
        for i in range(num_players):
            pseudo = input(f"Enter a pseudonym for Player {i+1}: ")
            self.players.append(Player(pseudo))
        print(f"{num_players} players have been added.")

    def load_backlog(self, filepath):

        """@brief Loads backlog items from a JSON file.
        @param filepath The path to the JSON file containing the backlog."""
        try:
            with open(filepath, "r") as file:
                self.backlog = json.load(file).get("tasks", [])
            print("Backlog loaded successfully.")
        except FileNotFoundError:
            print("Backlog file not found. Starting with an empty backlog.")
            self.backlog = []

    def save_game_state(self, filepath="data/game_state.json"):

        """@brief Save the current game state (backlog and player votes) to a file.
        @param filepath The path to the file to save the game state."""


        game_state = {
            "backlog": self.backlog,
            "players": [{"pseudo": player.pseudo, "vote": player.current_vote} for player in self.players]
        }
        with open(filepath, "w") as file:
            json.dump(game_state, file, indent=4)
        print("Game state saved.")


    def check_for_cafe_card(self):
            """ @brief Check if all players have chosen the 'joker' card.
            @return True if all players have chosen the 'joker' card, False otherwise.
            """
            if all(player.current_vote == "joker" for player in self.players):
                print("All players chose the 'joker' card! Saving game state.")
                self.save_game_state()
                return True
            return False

    def start_game(self):
        """@brief Main loop for running the game, where each player votes on each feature.
        @brief Process the backlog of features and collect votes from players.
        @brief Validate each feature based on the chosen rules.
        @brief Save the final report with validated features and their estimated difficulty.


        """
        
        # Ensure there is a backlog to process
        if not self.backlog:
            print("No tasks in backlog to vote on.")
            return
        
        # Loop through each feature in the backlog
        for feature in self.backlog:
            self.current_feature = feature
            print(f"\nCurrent feature: {feature['description']}")
            
            # Collect votes from each player for the current feature
            while True:
                self.collect_votes()
            
                # Check the votes and validate the feature
                if self.process_votes():
                    feature["validated"] = True
                    print(f"Feature '{feature['description']}' validated!")
                    break
                else: # Revote required
                    feature["validated"] = False
                    print(f"Feature '{feature['description']}' not validated.")

                    print("Please revote:")
                    self.reset_votes()

                
            # If all players chose the cafe card, save the state
            if self.check_for_cafe_card():
                break
        if all(task.get("validated", False) for task in self.backlog):
            print("\nAll features validated. Saving final report...")
            self.save_final_report()
    
    def reset_votes(self):
        """@brief Reset the votes for all players to allow revoting.
        """
        for player in self.players:
            player.reset_vote()


    def collect_votes(self):
        """@brief Collects votes from each player for the current feature.
        
        """
        for player in self.players:
            while True:
                #Game.timeout(player.pseudo)
                print(f"{player.pseudo}, available cards: {', '.join(player.cards)}")
                card = input(f"{player.pseudo}, choose a card: ")
                try:
                    player.vote(card)
                    break  # Exit the loop if the vote is valid
                except ValueError as e:
                    print(e)  # Ask for input again if card is invalid

    def process_votes(self):
        """@brief Process the votes based on the chosen rules.
        @return True if the feature is validated, False otherwise.
        
        """
        print("\nVotes collected:")

        difficulty=None
        
        votes = [player.current_vote for player in self.players]
        print(f"Votes: {votes}")
        
        if self.rules == "strict":
            # Unanimité : Tous les votes doivent être égaux
            if len(set(votes)) == 1:
                print("Unanimity reached! Feature validated.")
                difficulty = int(votes[0])
            else:
                print("No unanimity. Feature not validated. Revote required.")
                return False
        elif self.rules == "average":
            # Moyenne : Calcul de la moyenne des votes numériques
            valid_votes = [int(vote) for vote in votes if vote != "joker"]
            if valid_votes:
                difficulty = sum(valid_votes) / len(valid_votes)
                print(f"Average vote: {difficulty}")
            else:
                print("No valid votes to calculate an average.")
        elif self.rules == "median":
            # Médiane : Calcul de la médiane
                valid_votes = [int(vote) for vote in votes if vote != "joker"]
                if valid_votes:
                    sorted_votes = sorted(valid_votes)
                    mid = len(sorted_votes) // 2
                    if len(sorted_votes) % 2 == 0:
                        difficulty = (sorted_votes[mid - 1] + sorted_votes[mid]) / 2
                    else:
                        difficulty = sorted_votes[mid]
                    print(f"Median vote: {difficulty}")
                else:
                    print("No valid votes to calculate a median.")
        elif self.rules == "absolute_majority": # Majorité absolue
            from collections import Counter
            vote_count = Counter(votes)
            max_vote, max_count = vote_count.most_common(1)[0]
            if max_count > len(self.players) / 2:
                difficulty = int(max_vote)
                print(f"Absolute majority reached with card {difficulty}. Feature validated!")
                return True
            print("No absolute majority. Revote required.")
            return False
        elif self.rules == "relative_majority": # Majorité relative
            from collections import Counter
            vote_count = Counter(votes)
            max_vote, max_count = vote_count.most_common(1)[0]
            difficulty = int(max_vote)
            print(f"Relative majority reached with card {difficulty}. Feature validated!")
            return True

        else:
            print("No valid rule selected.")
        
        # Réinitialiser les votes pour le prochain tour
        if difficulty is not None:
            self.current_feature["difficulty"] = difficulty
            print(f"Difficulty for feature '{self.current_feature['description']}' set to: {difficulty}")

        for player in self.players:
            player.reset_vote()
        return True
    
    def load_game_state(self, filepath):
        """@brief Load the game state from a file.
        @param filepath The path to the file containing the game state.
        @throws FileNotFoundError if the file is not found.
        @throws ValueError if the file is corrupted or invalid.
        """ 
        try: # Load the game state from a file
            with open(filepath, "r") as file:
                data = json.load(file)
             # Load backlog
            self.backlog = data.get("backlog", [])
            if not self.backlog:
                print("Backlog is empty in the save file.")

            self.players = []
            for player_data in data.get("players", []):
                player = Player(player_data["pseudo"])
                player.current_vote = player_data.get("vote", "")
                self.players.append(player)

            print("Game state loaded successfully.")
        except FileNotFoundError:
            raise FileNotFoundError("Le fichier de sauvegarde est introuvable.")
        except json.JSONDecodeError:
            raise ValueError("Le fichier de sauvegarde est corrompu ou invalide.")
        if not self.backlog:
            print("No tasks in backlog to vote on.")
            return

        if not self.players:
            print("No players loaded. Please start a new game.")
            return


    def save_final_report(self, filepath="data/final_report.json"):
        """@brief Save the final report of validated features with their estimated difficulty.
        @param filepath The path to the file to save the final report.
        
        """
        report = {"tasks": self.backlog}  # Save the entire backlog with updates
        print("Saving final report:", report)  # Debug print
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(report, file, ensure_ascii=False, indent=4)
        print("Final report saved.")
        
