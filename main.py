# main.py

from models.players import Player

# Create a sample player
player1 = Player("Alice")

# Player votes with a card
player1.vote("5")

# Display the current vote
print(f"{player1.pseudo}'s vote is: {player1.current_vote}")

# Reset vote and check again
player1.reset_vote()
print(f"After reset, {player1.pseudo}'s vote is: {player1.current_vote}")
