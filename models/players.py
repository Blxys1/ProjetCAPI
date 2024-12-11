
class Player:
    """
    @class Player
    @brief Represents a player in the Planning Poker game.

    """
    def __init__(self, pseudo):
        """ @brief Constructor for the Player class.

        @param pseudo The player's pseudonym.
        """
        self.pseudo = pseudo  # Player's pseudonym
        self.current_vote = None  # Current card chosen by player (e.g., "5", "8", "joker")
        self.cards = ["1", "2", "3", "5", "8", "13", "20", "40", "100", "joker"]  # Example cards

    def vote(self, card):

        """Allows the player to vote by selecting a card.
        
        @param card The card chosen by the player.
        @throws ValueError if the card is not in the player's list of cards.

        """
        if card in self.cards:
            self.current_vote = card
            print(f"{self.pseudo} has voted with card {card}")
        else:
            raise ValueError(f"Invalid card: {card}")

    def reset_vote(self):
        """Clears the current vote for the player (used if a revote is needed).
        @brief Resets the player's vote to None.
        """
        self.current_vote = None 

