from collections import defaultdict

import numpy as np
from tqdm import tqdm

from blackjack_game import AutoBlackjackGame
from game_utils import enumerate_states, get_all_states


class BlackjackPolicy:
    def __init__(self):
        self.states = get_all_states()

        # mask the trivial states
        trivial_mask = []
        for player_hand_value, *_ in self.states:
            trivial_mask.append(player_hand_value < 12)
        self.trivial_mask = np.array(trivial_mask)

        # a probability function given an input state and action
        self.soft_policy_fn = np.zeros((len(self.states), 2))

        # always choose to hit given a trivial state (value less than 12)
        self.soft_policy_fn[self.trivial_mask, 1] = 1.0

        # random probability distributions over the non-trivial states
        n_nontrivial = len(self.states) - self.trivial_mask.sum()
        self.soft_policy_fn[~self.trivial_mask] = np.random.rand(n_nontrivial, 2)
        self.soft_policy_fn /= self.soft_policy_fn.sum(axis=1).reshape(-1, 1)

    def __call__(self, state_id):
        player_hand_value, *_ = self.states[state_id]
        if player_hand_value < 12:
            return True
        elif player_hand_value == 21:
            return False
        else:
            action_probs = self.soft_policy_fn[state_id]
            return np.random.choice([False, True], p=action_probs)


class OnPolicyMonteCarlo:
    def __init__(self):
        # initiate the game and policy
        self.policy = BlackjackPolicy()
        self.game = AutoBlackjackGame(self.policy)

        # gather the set of trivial states (i.e. always choose to hit on these states)
        self.trivial_states = set()
        for (player_hand_value, *_), i in enumerate_states().items():
            if player_hand_value < 12:
                self.trivial_states.add(i)

    def __call__(self, n_episodes, eps=0.01):
        n_states = len(get_all_states())
        n_actions = 2  # hit or stick
        q_table = np.zeros((n_states, n_actions))
        returns = defaultdict(list)

        n_played = 0
        # while n_played < n_episodes:
        for _ in tqdm(range(n_episodes)):
            # get the game history (sequence of states, actions, and rewards taken)
            states, actions, rewards = self.game.play()
            state_action_pairs = list(zip(states, actions))

            # old_probs = self.policy.soft_policy_fn.copy()
            # print(states)
            # print(actions)
            # print(rewards)
            # print()

            if len(states) > 0:
                n_played += 1

                g = 0
                for i in -np.arange(len(states))[::-1]:
                    s_i = states[i]
                    a_i = actions[i]
                    r_i = rewards[i]

                    if s_i not in self.trivial_states:
                        g += r_i
                        if (s_i, a_i) not in state_action_pairs[:i]:
                            returns[(s_i, a_i)].append(g)
                            q_table[s_i, a_i] = np.mean(returns[(s_i, a_i)])
                            optimal_action = np.argmax(q_table[s_i, :])

                            for a in (0, 1):
                                if a == optimal_action:
                                    update = 1 - (eps / 2)
                                else:
                                    update = eps / 2
                                self.policy.soft_policy_fn[s_i, a] = update


if __name__ == '__main__':
    mc = OnPolicyMonteCarlo()
    mc(10000)
    print(mc.policy.soft_policy_fn)

    # state_space = get_all_states()
    # policy_fn = BlackjackPolicy()
    # for state in state_space:
    #     print(state)
    #     print(policy_fn(state))
    #     print()
