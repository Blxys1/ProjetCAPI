# main.py

from models.players import Player

# Create a sample player
pseudo = input("Enter player's pseudo: ")

player1 = Player(pseudo)

# Display available cards for voting
print("Available cards for voting:", ", ".join(player1.cards))

# Ask the player to input their vote
card = input("Enter player's vote (choose from cards: 1, 2, 3, 5, 8, 13, 20, 40, 100, joker): ")

# Call the vote method on player1 with the card they chose, handling invalid input
try:
    player1.vote(card)  # Pass the chosen card to the vote method
except ValueError as e:
    print(e)  # Print the error message if the card is invalid

# Reset vote and check again
player1.reset_vote()
print(f"After reset, {player1.pseudo}'s vote is: {player1.current_vote}")
