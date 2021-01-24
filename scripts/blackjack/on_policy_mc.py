from collections import defaultdict
import json

import numpy as np
from tqdm import tqdm

from blackjack_game import AutoBlackjackGame
from game_utils import *

N_STATES = 180
N_ACTIONS = 2
N_EPISODES = 500000


def nontrivial_state(state):
    player_value, *_ = state
    return 11 < player_value < 21


def random_prob_init(shape):
    probs = np.random.rand(*shape)
    probs /= probs.sum(axis=1).reshape((-1, 1))
    return probs


class BlackjackPolicy:
    def __init__(self):
        self.soft_policy_fn = random_prob_init((N_STATES, N_ACTIONS))
        self.state_to_idx = enumerate_states()

    def __call__(self, state):
        """Choose an action given a state

        Parameters
        ----------
        state: tuple

        Returns
        -------
        bool
            If true then hit, else stick
        """
        player_value, *_ = state
        # fixed policy when player hand value is less than 12 (always hit)
        if player_value < 12:
            return True
        # always stick on a blackjack
        if player_value == 21:
            return False
        # otherwise use the soft policy function
        idx = self.state_to_idx.get(state)
        if idx is not None:
            action_probs = self.soft_policy_fn[idx]
            return np.random.choice([False, True], p=action_probs)
        else:
            raise ValueError(f'Invalid State: {state}')


class OnPolicyMonteCarlo:
    def __init__(self):
        # initiate the game and policy
        self.policy = BlackjackPolicy()
        self.game = AutoBlackjackGame(self.policy)
        self.state_to_idx = enumerate_states()

    def run(self, n_episodes, eps=0.01):
        q_table = np.zeros((N_STATES, N_ACTIONS))
        returns = defaultdict(list)

        for _ in tqdm(range(n_episodes), desc='On-policy Monte Carlo'):

            # get the game history (sequence of states, actions, and rewards taken)
            states, actions, rewards = self.game.play()
            state_action_pairs = list(zip(states, actions))

            if len(states) > 0:
                g = 0
                for i in -np.arange(len(states))[::-1]:
                    # print(i)
                    s_i = states[i]
                    a_i = actions[i]
                    r_i = rewards[i]
                    pair = (s_i, a_i)
                    if nontrivial_state(s_i):
                        g += r_i
                        if pair not in state_action_pairs[:i]:
                            state_idx = self.state_to_idx[s_i]
                            action_idx = int(a_i)

                            returns[pair].append(g)
                            q_table[state_idx, action_idx] = np.mean(returns[pair])
                            optimal_action = np.argmax(q_table[state_idx, :])

                            for a in (0, 1):
                                if a == optimal_action:
                                    update = 1 - (eps / 2)
                                else:
                                    update = eps / 2
                                self.policy.soft_policy_fn[state_idx, int(a)] = update
        return q_table


def main():
    monte_carlo = OnPolicyMonteCarlo()
    action_values = monte_carlo.run(N_EPISODES)

    # store the policy
    optimal_policy_json = []
    states = get_all_states()
    for (player_val, dealer_val, usable_ace), (p_stick, p_hit) in zip(states, monte_carlo.policy.soft_policy_fn):
        optimal_policy_json.append({
            'player_hand_value': player_val,
            'dealer_card_value': dealer_val,
            'usable_ace': usable_ace,
            'hit': bool(p_hit > p_stick)
        })
    with open('optimal-policy.json', 'w') as file:
        json.dump(optimal_policy_json, file)

    # store the action-value table
    optimal_action_value_json = []
    for (player_val, dealer_val, usable_ace), (q_stick, q_hit) in zip(states, action_values):
        optimal_action_value_json.append({
            'player_hand_value': player_val,
            'dealer_card_value': dealer_val,
            'usable_ace': usable_ace,
            'q_stick': q_stick,
            'q_hit': q_hit
        })
    with open('optimal-action-values.json', 'w') as file:
        json.dump(optimal_action_value_json, file)


if __name__ == '__main__':
    main()
