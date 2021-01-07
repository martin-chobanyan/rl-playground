"""Exercise 4.9 (Gambler Problem)

- Gambler stakes X money on a coin flip
- Heads means they win X, tails means they lose X
- Game is won if total winnings reach $100, lost if it reaches $0
- State is gambler's capital {1, 2, ..., 99}
- Actions are stakes {0, 1, ... min(s, 100-s)} where s is the current capital
- Reward is +1 for winning, 0 for all other actions
- Undiscounted, episodic, finite MDP
"""

import matplotlib.pyplot as plt
import numpy as np


def get_max_stake(capital, goal):
    """Define the maximum stake (action) which can be made given the current capital (state)

    Parameters
    ----------
    capital: int
    goal: int

    Returns
    -------
    int
    """
    return min(capital, goal - capital)


def calculate_action_values(coin_env, values, state):
    """Calculate the action-values

    Parameters
    ----------
    coin_env: CoinFlipEnvironment
    values: numpy.ndarray
    state: int

    Returns
    -------
    list[int]
    """
    action_values = []
    for action in range(1, get_max_stake(state, coin_env.goal) + 1):
        action_val = 0

        # option 1: heads -> win
        p = coin_env.p_head
        new_state = state + action
        v = values[new_state]
        reward = coin_env.get_reward(new_state)
        action_val += p * (reward + v)

        # option 2: tails -> lose
        p = 1 - coin_env.p_head
        new_state = state - action
        v = values[new_state]
        reward = coin_env.get_reward(new_state)
        action_val += p * (reward + v)

        action_values.append(action_val)
    return action_values


class CoinFlipEnvironment:
    def __init__(self, p_head, goal=100):
        """Initialization

        Parameters
        ----------
        p_head: float
        goal: int, optional
        """
        self.p_head = p_head
        self.goal = goal

    def get_reward(self, state):
        return 1 if state == self.goal else 0

    def transition(self, state, action):
        """Transition function

        Parameters
        ----------
        state: int
            The current state (total winnings)
        action: int
            The action / stake in dollars

        Returns
        -------
        int, int
            The next state (total winnings) and reward (+1 for $100 winnings)
        """
        max_stake = get_max_stake(state, self.goal)
        assert action >= 0, 'Stake must be non-negative!'
        assert action <= max_stake, 'Cannot make a stake that would lead to over $100 winnings!'

        if np.random.rand() < self.p_head:
            capital = state + action
        else:
            capital = state - action

        reward = 0
        if capital == self.goal:
            reward = 1
        return capital, reward


def value_iteration_solution(coin_env, value_threshold=1e-7):
    """Value Iteration solution to Gambler's Problem

    Parameters
    ----------
    coin_env: CoinFlipEnvironment
    value_threshold: float, optional

    Returns
    -------
    dict[int, int], numpy.ndarray
    """
    num_states = coin_env.goal + 1
    values = np.zeros(num_states)

    # value iteration: approximate the value function
    value_change = 1
    while value_change > value_threshold:
        value_change = 0
        old_values = values.copy()
        for state in range(1, num_states-1):
            values[state] = max(calculate_action_values(coin_env, values, state))
        value_change = max(value_change, np.abs(values - old_values).max())

    # defining the policy: map each state to an action
    policy = dict()
    for state in range(1, coin_env.goal):
        action_values = np.array(calculate_action_values(coin_env, values, state))
        policy[state] = action_values.argmax() + 1

    return policy, values


if __name__ == '__main__':
    states = range(1, 100)
    policy_fn, value_fn = value_iteration_solution(CoinFlipEnvironment(0.25))
    stakes_25 = [policy_fn[s] for s in states]
    values_25 = [value_fn[s] for s in states]

    policy_fn, value_fn = value_iteration_solution(CoinFlipEnvironment(0.4))
    stakes_40 = [policy_fn[s] for s in states]
    values_40 = [value_fn[s] for s in states]

    policy_fn, value_fn = value_iteration_solution(CoinFlipEnvironment(0.55))
    stakes_55 = [policy_fn[s] for s in states]
    values_55 = [value_fn[s] for s in states]

    fig, ((ax_p25, ax_p40), (ax_p55, ax_v)) = plt.subplots(2, 2)
    ax_p25.bar(states, stakes_25)
    ax_p25.set_title('Policy: P_head = 0.25')
    ax_p25.set_xlabel('Capital')
    ax_p25.set_ylabel('Stake')

    ax_p40.bar(states, stakes_40)
    ax_p40.set_title('Policy: P_head = 0.40')
    ax_p40.set_xlabel('Capital')
    ax_p40.set_ylabel('Stake')

    ax_p55.bar(states, stakes_55)
    ax_p55.set_title('Policy: P_head = 0.55')
    ax_p55.set_xlabel('Capital')
    ax_p55.set_ylabel('Stake')

    ax_v.plot(states, values_25, label='P_head = 0.25')
    ax_v.plot(states, values_40, label='P_head = 0.40')
    ax_v.plot(states, values_55, label='P_head = 0.55')
    ax_v.set_title('Value Functions')
    ax_v.set_xlabel('Capital')
    ax_v.set_ylabel('Value Estimates')

    plt.tight_layout()
    plt.legend()
    plt.show()
