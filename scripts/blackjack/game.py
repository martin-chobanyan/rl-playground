"""This file contains the main BlackjackGame object, a one-on-one game with no splitting or doubling-down"""

import random

CARDS = [
    '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
]

PLAYER_WIN = 1
DRAW_GAME = 0
PLAYER_LOSE = -1


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
    int
        The integer hand value (highest value is returned without going over 21 if an ace is present)
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
        alt_hand_value = hand_value + 10
        if alt_hand_value <= 21:
            return alt_hand_value
    return hand_value


def check_blackjack(hand):
    return get_hand_value(hand) == 21


def check_bust(hand):
    return get_hand_value(hand) > 21


def check_under_17(hand):
    return get_hand_value(hand) < 17


class BlackjackGame:
    def __init__(self, interactive=True):
        self.player_hand = []
        self.dealer_hand = []
        self.hidden_dealer = True
        self.interacive = interactive

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

    def show_current_state(self):
        if self.interacive:
            print('--------------------------------------')
            print(f'Your hand: {self.player_hand}')
            if self.hidden_dealer:
                print(f'Dealer hand: [{self.dealer_hand[0]}, ?]')
            else:
                print(f'Dealer hand: {self.dealer_hand}')
            print('--------------------------------------')

    def play(self):
        # deal the starting cards
        self.hidden_dealer = True
        self.deal_cards()
        self.show_current_state()

        # check for a natural hand
        player_turn = True
        if check_blackjack(self.player_hand):
            print("Blackjack! Let's see what the dealer has...")
            player_turn = False

        # player's turn
        if player_turn:
            end_turn = False
            while not end_turn:
                response = input('Would you like to hit (y/n)?')
                hit_me = self.parse_response(response)
                if hit_me:
                    self.hit_player()
                    if check_blackjack(self.player_hand):
                        print("Blackjack! Let's see what the dealer has...")
                        end_turn = True
                    elif check_bust(self.player_hand):
                        self.show_current_state()
                        return PLAYER_LOSE
                    self.show_current_state()
                else:
                    end_turn = True

        # dealer's turn
        self.hidden_dealer = False
        under_17 = check_under_17(self.dealer_hand)
        while under_17:
            self.show_current_state()
            print('Dealer chooses to hit...')
            self.hit_dealer()
            under_17 = check_under_17(self.dealer_hand)
        self.show_current_state()

        # check the dealer's final hand
        if check_bust(self.dealer_hand):
            return PLAYER_WIN
        else:
            player_hand_value = self.get_player_hand_value()
            dealer_hand_value = self.get_dealer_hand_value()
            if player_hand_value > dealer_hand_value:
                return PLAYER_WIN
            if player_hand_value < dealer_hand_value:
                return PLAYER_LOSE
            return DRAW_GAME


if __name__ == '__main__':
    game = BlackjackGame()
    result = game.play()

    if result == PLAYER_WIN:
        print('Congratulations, you won!')
    elif result == PLAYER_LOSE:
        print('Sorry, you lost!')
    elif result == DRAW_GAME:
        print('It looks like you tied!')
