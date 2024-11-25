from models.players import Player
from models.game import Game

# Create a sample game with 3 players
game = Game(num_players=3, rules="strict")

# Start the game (for now, it just initializes players and loads backlog)
game.start_game()   

# Save the game state to a file*
game.save_game_state()

