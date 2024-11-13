# models/player.py

class Player:
    def __init__(self, pseudo):
        self.pseudo = pseudo  # Player's pseudonym
        self.current_vote = None  # Current card chosen by player (e.g., "5", "8", "joker")
        self.cards = ["1", "2", "3", "5", "8", "13", "20", "40", "100", "joker"]  # Example cards

    def vote(self, card):
        """Allows the player to vote by selecting a card."""
        if card in self.cards:
            self.current_vote = card
            print(f"{self.pseudo} has voted with card {card}")
        else:
            raise ValueError(f"Invalid card: {card}")

    def reset_vote(self):
        """Clears the current vote for the player (used if a revote is needed)."""
        self.current_vote = None 

