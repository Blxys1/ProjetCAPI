from models.players import Player
from models.game import Game
import signal
import os

# Main menu
def signal_handler(game):
    """Signal handler to save the game state on interruption (Ctrl+C)."""
    print("\nInterruption detected! Saving the game state...")
    game.save_game_state("data/game_state.json")
    print("Game state saved. Exiting the game.")
    exit(0)

def main_menu():
    while True:
        print("Bienvenue dans l'application Planning Poker")
        print("1. Nouvelle partie")
        print("2. Charger une partie")
        print("3. Quitter")

        choice = input("Choisissez une option : ") # i want to loop in case the user gives smt other than 1 2 3 
        while True:
            if choice not in ["1", "2", "3"]:
                print("Choix invalide.")
                choice = input("Choisissez une option : ")
            
            else:
                break

        if choice == "1":
            num_players = int(input("Entrez le nombre de joueurs : "))
            while num_players <= 1:
                print("Nombre de joueurs invalide.")
                num_players = int(input("Entrez le nombre de joueurs : "))
            rules = input("Choisissez une règle (strict, average, median, absolute_majority, relative_majority) : ")
            while rules not in ["strict", "average", "median", "absolute_majority", "relative_majority"]:
                print("Règle invalide.")
                rules = input("Choisissez une règle (strict, average, median, absolute_majority, relative_majority) : ")
                
                # add rules if the players chooses smt wrong 
            
            game = Game(num_players=num_players, rules=rules)
            # Register signal handler to save state on interruption
            signal.signal(signal.SIGINT, lambda s, f: signal_handler(game))
            game.start_game()
        elif choice == "2":
            try:
                game = Game(num_players=0)  # Initialisation avec 0 joueurs
                game.load_game_state("data/game_state.json")
                game.start_game()

            except FileNotFoundError:
                print("Aucune sauvegarde trouvée. ")
            except Exception as e:
                print(f'Erreur lors du chargement de la partie {e}')
        elif choice == "3":
            print("Merci d'avoir utilisé Planning Poker. À bientôt !")
            break
     

if __name__ == "__main__":
    main_menu()
