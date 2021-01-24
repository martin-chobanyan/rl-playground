"""This file contains the main BlackjackGame object, a one-on-one game with no splitting or doubling-down"""

import time

from game_utils import *


class AbstractBlackjackGame:
    def __init__(self):
        self.player_hand = []
        self.dealer_hand = []
        self.hidden_dealer = True

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

    def play(self):
        raise NotImplementedError


class InteractiveBlackjackGame(AbstractBlackjackGame):
    @staticmethod
    def parse_response(response):
        if response.lower() in ['y', 'yes']:
            return True
        elif response.lower() in ['n', 'no']:
            return False
        else:
            raise ValueError('You must say yes or no')

    def show_hands(self):
        print('--------------------------------------')
        print(f'Your hand: {self.player_hand}')
        if self.hidden_dealer:
            print(f"Dealer hand: ['{self.dealer_hand[0]}', ?]")
        else:
            print(f'Dealer hand: {self.dealer_hand}')
        print('--------------------------------------')

    def play(self):
        # deal the starting cards
        self.hidden_dealer = True
        self.deal_cards()
        self.show_hands()

        # check for a natural hand
        if check_blackjack(self.player_hand):
            print("Blackjack! Let's see what the dealer has...")
        else:
            end_turn = False
            while not end_turn:
                response = input('Would you like to hit (yes/no)?')
                hit_me = self.parse_response(response)
                if hit_me:
                    self.hit_player()
                    if check_blackjack(self.player_hand):
                        end_turn = True
                        print("Blackjack! Let's see what the dealer has...")
                    elif check_bust(self.player_hand):
                        self.show_hands()
                        return PLAYER_LOSE
                    self.show_hands()
                else:
                    end_turn = True
                    print("You chose to stick. Let's see what the dealer has...")

        # dealer's turn
        self.hidden_dealer = False
        under_17 = check_under_17(self.dealer_hand)
        while under_17:
            self.show_hands()
            print('Dealer chooses to hit...')
            time.sleep(3)
            self.hit_dealer()
            under_17 = check_under_17(self.dealer_hand)
        self.show_hands()

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


class AutoBlackjackGame(AbstractBlackjackGame):
    def __init__(self, policy):
        super().__init__()
        self.policy = policy
        self.state_to_id = enumerate_states()

    def get_current_state(self):
        player_value = self.get_player_hand_value()
        visible_dealer_value = self.get_visible_dealer_value()
        usable_ace = has_usable_ace(self.player_hand)
        return player_value, visible_dealer_value, usable_ace

    def play(self):
        # deal the starting cards
        self.deal_cards()
        states = []
        actions = []
        rewards = []

        # end the game if the player has a natural hand (no point from a state-action perspective)
        if check_blackjack(self.player_hand):
            return states, actions, rewards
        else:
            end_turn = False
            while not end_turn:
                curr_state = self.get_current_state()
                hit_me = self.policy(curr_state)
                states.append(curr_state)
                actions.append(hit_me)
                rewards.append(0)

                if hit_me:
                    self.hit_player()
                    if check_blackjack(self.player_hand):
                        end_turn = True
                    elif check_bust(self.player_hand):
                        rewards[-1] = PLAYER_LOSE
                        return states, actions, rewards
                else:
                    end_turn = True

        # dealer's turn
        under_17 = check_under_17(self.dealer_hand)
        while under_17:
            self.hit_dealer()
            under_17 = check_under_17(self.dealer_hand)

        # check the dealer's final hand
        if check_bust(self.dealer_hand):
            rewards[-1] = PLAYER_WIN
            return states, actions, rewards
        else:
            player_hand_value = self.get_player_hand_value()
            dealer_hand_value = self.get_dealer_hand_value()

            if player_hand_value > dealer_hand_value:
                rewards[-1] = PLAYER_WIN
                return states, actions, rewards

            if player_hand_value < dealer_hand_value:
                rewards[-1] = PLAYER_LOSE
                return states, actions, rewards
        return states, actions, rewards


if __name__ == '__main__':
    game = InteractiveBlackjackGame()
    result = game.play()
    print_result(result)

    # game = AutoBlackjackGame(lambda x: random.choice([True, False]))
    # history = game.play()
    # states = history[0]
    # actions = history[1]
    # rewards = history[2]
    # for s, a, r in zip(states, actions, rewards):
    #     print(s.get_state_tuple())
    #     print(a)
    #     print(r)
    #     print()
