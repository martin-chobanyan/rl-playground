from collections import defaultdict
import os
from random import choice
import json

import numpy as np
from tqdm import tqdm

from blackjack_game import AutoBlackjackGame
from game_utils import *

N_STATES = 180
N_ACTIONS = 2
N_EPISODES = 2000000


def nontrivial_state(state):
    player_value, *_ = state
    return 11 < player_value < 21


def random_prob_init(shape):
    probs = np.random.rand(*shape)
    probs /= probs.sum(axis=1).reshape((-1, 1))
    return probs


class ReturnsAverage:
    def __init__(self):
        self.avg = 0
        self.count = 0

    def add_return(self, r):
        self.avg = (self.count * self.avg + r) / (self.count + 1)
        self.count += 1


class BlackjackPolicy:
    def __init__(self, explore=True):
        self.explore = explore
        self.states = get_all_states()
        self.actions = [False, True]
        self.policy_dict = {state: choice(self.actions) for state in self.states}

    def reset_explore(self):
        self.explore = True

    def __call__(self, state):
        player_value, *_ = state
        # fixed policy when player hand value is less than 12 (always hit)
        if player_value < 12:
            return True
        # always stick on a blackjack
        if player_value == 21:
            return False
        # if exploring, return a random action
        if self.explore:
            self.explore = False
            return choice(self.actions)
        # otherwise get the action from the policy dict
        return self.policy_dict[state]


class OnPolicyMonteCarlo:
    def __init__(self):
        # initiate the game and policy
        self.policy = BlackjackPolicy()
        self.game = AutoBlackjackGame(self.policy)
        self.state_to_idx = enumerate_states()

    def run(self, n_episodes):
        q_table = np.zeros((N_STATES, N_ACTIONS))
        returns = defaultdict(ReturnsAverage)

        for _ in tqdm(range(n_episodes), desc='Monte Carlo with exploring starts'):

            # get the game history (sequence of states, actions, and rewards taken)
            self.policy.reset_explore()
            states, actions, rewards = self.game.play()
            state_action_pairs = list(zip(states, actions))

            if len(states) > 0:
                g = 0
                for i in -np.arange(len(states))[::-1]:
                    s_i = states[i]
                    a_i = actions[i]
                    r_i = rewards[i]
                    pair = (s_i, a_i)
                    if nontrivial_state(s_i):
                        g += r_i
                        if pair not in state_action_pairs[:i]:
                            state_idx = self.state_to_idx[s_i]
                            action_idx = int(a_i)

                            returns[pair].add_return(g)
                            q_table[state_idx, action_idx] = returns[pair].avg
                            self.policy.policy_dict[s_i] = bool(np.argmax(q_table[state_idx, :]))
        return q_table


def main():
    monte_carlo = OnPolicyMonteCarlo()
    action_values = monte_carlo.run(n_episodes=N_EPISODES)

    # store the policy
    optimal_policy_json = []
    for (player_val, dealer_val, usable_ace), hit_me in monte_carlo.policy.policy_dict.items():
        optimal_policy_json.append({
            'player_hand_value': player_val,
            'dealer_card_value': dealer_val,
            'usable_ace': usable_ace,
            'hit': hit_me
        })
    with open(os.path.join('scripts', 'blackjack', 'optimal-policy.json'), 'w') as file:
        json.dump(optimal_policy_json, file)

    # store the action-value table
    optimal_action_value_json = []
    states = get_all_states()
    for (player_val, dealer_val, usable_ace), (q_stick, q_hit) in zip(states, action_values):
        optimal_action_value_json.append({
            'player_hand_value': player_val,
            'dealer_card_value': dealer_val,
            'usable_ace': usable_ace,
            'q_stick': q_stick,
            'q_hit': q_hit
        })
    with open(os.path.join('scripts', 'blackjack', 'optimal-action-values.json'), 'w') as file:
        json.dump(optimal_action_value_json, file)


if __name__ == '__main__':
    main()
