"""This file contains the main BlackjackGame object"""

import random

CARDS = [
    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
]


def get_card_value(card):
    """Get the blackjack value of a card

    Parameters
    ----------
    card: str

    Returns
    -------
    int
    """
    try:
        return int(card)
    except ValueError:
        if card == 'A':
            return 1  # this can also be treated as an eleven
        return 10


class BlackjackGame:
    def __init__(self):
        self.player_hand = []
        self.player_values = []

        self.dealer_visible = None
        self.dealer_hidden = None

        self.dealer_visible_value = 0
        self.dealer_hidden_value = 0

    @staticmethod
    def draw_card():
        """Draw a random card (no suits) from an infinite deck of cards

        Returns
        -------
        str
        """
        return random.choice(CARDS)

    def deal_cards(self):
        """Deal the starting cards to both the player and the dealer"""
        self.player_hand = [self.draw_card(), self.draw_card()]
        self.player_values = [get_card_value(c) for c in self.player_hand]

        self.dealer_visible = self.draw_card()
        self.dealer_hidden = self.draw_card()

        self.dealer_visible_value = get_card_value(self.dealer_visible)
        self.dealer_hidden_value = get_card_value(self.dealer_hidden)

    def start_game(self):
        self.deal_cards()


if __name__ == '__main__':
    game = BlackjackGame()
    game.start_game()
    print(game.player_hand)
    print(game.player_values)
    print()
