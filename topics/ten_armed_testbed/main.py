"""Run 2000 10-arm bandit problems with the sample-average action-value method"""

import matplotlib.pyplot as plt
import numpy as np


def sample_average_estimate(rewards, actions):
    """Sample-average method for estimating action values

    Qt(a) := (sum of rewards when a taken prior to t) / (# of times a taken prior to t)

    Parameters
    ----------
    rewards: numpy.ndarray
        The array of rewards
    actions: numpy.ndarray
        The array of actions taken (actions must be labeled 0, ... n-1)

    Returns
    -------
    list[float]
        The list of estimate action values per action
    """
    value_estimates = []
    n_actions = len(set(actions))
    for a in range(n_actions):
        mask = (actions == a)
        action_val = rewards[mask].sum() / mask.sum()
        value_estimates.append(action_val)
    return value_estimates


def run_10_arm_bandit(n_steps):
    # sample the true q* value per action from a unit Gaussian
    exp_action_vals = np.random.randn(10)

    actions = []
    rewards = []
    for _ in range(n_steps):
        pass
    return


if __name__ == '__main__':
    r = np.array([10, -10, 20, 90, 10, -20])
    a = np.array([0, 1, 0, 2, 0, 1])
    x = sample_average_estimate(r, a)
    print(x)
    print()
