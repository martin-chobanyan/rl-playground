"""Run 2000 10-arm bandit problems with the sample-average action-value method"""

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


def sample_average_estimate(rewards, actions, n_unique_actions):
    """Sample-average method for estimating action values

    Qt(a) := (sum of rewards when a taken prior to t) / (# of times a taken prior to t)

    Parameters
    ----------
    rewards: numpy.ndarray
        The array of rewards
    actions: numpy.ndarray
        The array of actions taken (actions must be labeled 0, ... n-1)
    n_unique_actions: int
        The number of possible unique actions

    Returns
    -------
    numpy.ndarray
        The list of estimate action values per action
    """
    value_estimates = []
    for a in range(n_unique_actions):
        mask = (actions == a)
        numerator = rewards[mask].sum()
        denominator = mask.sum()
        value_estimates.append(numerator / denominator if denominator != 0 else 0)
    return np.array(value_estimates)


def run_k_arm_bandit(n_steps, n_arms):
    # sample the true q* value per action from a unit Gaussian
    true_action_vals = np.random.randn(n_arms)

    # sample the rewards per action for each step
    # resulting array will have shape (n_steps, n_arms)
    sample_rewards = np.stack([np.random.normal(q_a, 1, n_steps) for q_a in true_action_vals]).T

    actions_taken = []
    rewards_received = []
    values = np.zeros(n_arms)
    for rewards in sample_rewards:
        # select the action with the highest current estimated value
        action = values.argmax()
        actions_taken.append(action)
        rewards_received.append(rewards[action])

        # update the estimated action-values using the sample average
        values = sample_average_estimate(rewards=np.array(rewards_received),
                                         actions=np.array(actions_taken),
                                         n_unique_actions=n_arms)

    return actions_taken, rewards_received, true_action_vals


def run_ten_armed_testbed(n_runs=50, n_steps=1000):
    # run the experiments
    actions = []
    rewards = []
    true_action_values = []
    for _ in tqdm(range(n_runs)):
        a, r, tav = run_k_arm_bandit(n_steps=n_steps, n_arms=10)
        actions.append(a)
        rewards.append(r)
        true_action_values.append(tav)
    actions = np.stack(actions)
    rewards = np.stack(rewards)
    true_action_values = np.stack(true_action_values)

    # first plot: average reward over time

    mean_reward_per_step = rewards.mean(axis=0)

    fig, ax = plt.subplots()
    ax.plot(range(n_steps), mean_reward_per_step)
    plt.show()


if __name__ == '__main__':
    # r = np.array([10, -10, 20, 90, 10, -20])
    # a = np.array([0, 1, 0, 2, 0, 1])
    # x = sample_average_estimate(r, a)
    # print(x)
    run_ten_armed_testbed()
