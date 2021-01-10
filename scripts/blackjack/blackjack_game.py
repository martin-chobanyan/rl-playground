"""This file contains the main BlackjackGame object, a one-on-one game with no splitting or doubling-down"""

import random

from game_utils import display_game_history

CARDS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

# game result codes
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


def get_hand_value(hand, ace_equals_one=False):
    """Get the blackjack value of a hand

    Parameters
    ----------
    hand: list[str]
        A list of the string card identifiers
    ace_equals_one: bool, optional
        If true, then all Aces will be counted as ones

    Returns
    -------
    int
        The integer hand value (highest value is returned without going over 21 if an ace is present)
    """
    hand_value = 0
    has_ace = False
    for card in hand:
        try:
            card_value = int(card)
        except ValueError:
            if card == 'A':
                has_ace = True
                card_value = 1
            else:
                card_value = 10
        hand_value += card_value
    if has_ace and not ace_equals_one:
        alt_hand_value = hand_value + 10
        if alt_hand_value <= 21:
            return alt_hand_value
    return hand_value


def has_usable_ace(hand):
    """Checks if a hand contains a usable ace (one that can be counted as an 11 without busting)

    Parameters
    ----------
    hand: list[str]

    Returns
    -------
    bool
    """
    has_ace = any(card == 'A' for card in hand)
    hand_value = get_hand_value(hand, ace_equals_one=True)
    return has_ace and (hand_value + 10 <= 21)


def check_blackjack(hand):
    return get_hand_value(hand) == 21


def check_bust(hand):
    return get_hand_value(hand) > 21


def check_under_17(hand):
    return get_hand_value(hand) < 17


def print_result(game_result):
    if game_result == PLAYER_WIN:
        print('Congratulations, you won!')
    elif game_result == PLAYER_LOSE:
        print('Sorry, you lost!')
    elif game_result == DRAW_GAME:
        print('It looks like you tied!')
    print()


class BlackjackGame:
    def __init__(self):
        self.player_hand = []
        self.dealer_hand = []
        self.hidden_dealer = True

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

    def get_visible_dealer_value(self):
        return get_hand_value([self.dealer_hand[0]])

    def hit_player(self):
        card = draw_card()
        self.player_hand.append(card)

    def hit_dealer(self):
        card = draw_card()
        self.dealer_hand.append(card)

    def get_state(self):
        return self.get_player_hand_value(), self.get_visible_dealer_value(), has_usable_ace(self.player_hand)

    def show_hands(self, interactive):
        if interactive:
            print('--------------------------------------')
            print(f'Your hand: {self.player_hand}')
            if self.hidden_dealer:
                print(f"Dealer hand: ['{self.dealer_hand[0]}', ?]")
            else:
                print(f'Dealer hand: {self.dealer_hand}')
            print('--------------------------------------')

    def play(self, policy_fn=None):
        # set up
        interactive = (policy_fn is None)
        states = []
        actions = []
        rewards = []

        # deal the starting cards
        self.hidden_dealer = True
        self.deal_cards()
        self.show_hands(interactive=interactive)

        # check for a natural hand
        if check_blackjack(self.player_hand):
            if interactive:
                print("Blackjack! Let's see what the dealer has...")
        else:
            end_turn = False
            while not end_turn:
                states.append(self.get_state())
                if interactive:
                    response = input('Would you like to hit (yes/no)?')
                    hit_me = self.parse_response(response)
                else:
                    hit_me = policy_fn(states[-1])
                actions.append(hit_me)
                rewards.append(0)

                if hit_me:
                    self.hit_player()
                    if check_blackjack(self.player_hand):
                        end_turn = True
                        if interactive:
                            print("Blackjack! Let's see what the dealer has...")
                    elif check_bust(self.player_hand):
                        self.show_hands(interactive=interactive)
                        rewards[-1] = PLAYER_LOSE
                        return PLAYER_LOSE, (states, actions, rewards)
                    self.show_hands(interactive=interactive)
                else:
                    end_turn = True

        # dealer's turn
        self.hidden_dealer = False
        under_17 = check_under_17(self.dealer_hand)
        while under_17:
            self.show_hands(interactive=interactive)
            print('Dealer chooses to hit...')
            self.hit_dealer()
            under_17 = check_under_17(self.dealer_hand)
        self.show_hands(interactive=interactive)

        # check the dealer's final hand
        if check_bust(self.dealer_hand):
            rewards[-1] = PLAYER_WIN
            return PLAYER_WIN, (states, actions, rewards)
        else:
            player_hand_value = self.get_player_hand_value()
            dealer_hand_value = self.get_dealer_hand_value()

            if player_hand_value > dealer_hand_value:
                rewards[-1] = PLAYER_WIN
                return PLAYER_WIN, (states, actions, rewards)

            if player_hand_value < dealer_hand_value:
                rewards[-1] = PLAYER_LOSE
                return PLAYER_LOSE, (states, actions, rewards)

            return DRAW_GAME, (states, actions, rewards)


if __name__ == '__main__':
    game = BlackjackGame()
    result, history = game.play()
    print_result(result)
    display_game_history(*history)
