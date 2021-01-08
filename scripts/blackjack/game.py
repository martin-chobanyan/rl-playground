"""This file contains the main BlackjackGame object"""

import random

CARDS = [
    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
]


def draw_card():
    """Draw a random card (no suits) from an infinite deck of cards

    Returns
    -------
    str
    """
    return random.choice(CARDS)


def get_hand_value(hand):
    """Get the blackjack value of a hand

    Parameters
    ----------
    hand: list[str]
        A list of the string card identifiers

    Returns
    -------
    int or tuple
        The integer value except if a usable ace is present, in which case it is a tuple of two possible values
    """
    hand_value = 0
    ace = False
    for card in hand:
        try:
            card_value = int(card)
        except ValueError:
            if card == 'A':
                ace = True
                card_value = 1
            else:
                card_value = 10
        hand_value += card_value
    if ace:
        return hand_value, hand_value + 10
    return hand_value


class BlackjackGame:
    def __init__(self):
        self.player_hand = []
        self.dealer_hand = []

    @staticmethod
    def parse_response(response):
        if response.lower() in ['y', 'yes']:
            return True
        elif response.lower() in ['n', 'no']:
            return False
        else:
            raise ValueError('You must say yes or no')

    def deal_cards(self):
        """Deal the starting cards to both the player and the dealer"""
        self.player_hand = [draw_card(), draw_card()]
        self.dealer_hand = [draw_card(), draw_card()]

    def get_player_hand_value(self):
        return get_hand_value(self.player_hand)

    def get_dealer_hand_value(self):
        return get_hand_value(self.dealer_hand)

    def hit_player(self):
        card = draw_card()
        self.player_hand.append(card)

    def hit_dealer(self):
        card = draw_card()
        self.dealer_hand.append(card)

    def start_game(self):
        self.deal_cards()
        print(self.player_hand)
        print(self.dealer_hand)

        finished_game = False
        player_turn = True
        while not finished_game:
            if player_turn:
                response = input('Would you like to hit (y/n)?')
                hit_me = self.parse_response(response)
                if hit_me:
                    print('Hit!')
                else:
                    print('Stick!')
            else:
                pass


if __name__ == '__main__':
    game = BlackjackGame()
    # game.start_game()

    for _ in range(10):
        hand = [draw_card(), draw_card(), draw_card()]
        print(hand)
        print(get_hand_value(hand))
        print()
    print()
