"""Run the modified ten-armed bandit testbed as specified in exercise 2.5"""

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


def run_nonstationary_k_arm_bandit(n_steps, n_arms, eps, alpha=None):
    """Run the K-arm bandit problem

    Parameters
    ----------
    n_steps: int
        The number of steps to run
    n_arms: int
        The number of arms (actions) in the problem
    eps: float
        The exploration probability
    alpha: float, optional
        The scaling factor. If left as None, then the scaling factor is defined as a_n(a) = 1/n

    Returns
    -------
    A tuple of the actions taken, rewards received, and the true action-values
    """
    qn_per_action = np.zeros(n_arms)
    action_counts = np.zeros(n_arms)

    # sample the true q* value per action from a unit Gaussian
    true_action_vals = np.random.randn(n_arms)

    actions_taken = []
    rewards_received = []
    for _ in range(n_steps):
        # exploration: choose random action with probability `eps`
        if np.random.rand() < eps:
            action = np.random.randint(0, n_arms)
        # exploitation: select the action with the highest current estimated value
        else:
            action = qn_per_action.argmax()

        # add some noise to the true action-values
        true_action_vals += np.random.normal(0, 0.01, n_arms)

        # sample the reward from this selected action
        curr_reward = np.random.normal(true_action_vals[action], 1)

        # update the action count
        action_counts[action] += 1
        n = action_counts[action]

        # calculate the scaling factor if it is None
        alpha_val = (1 / n) if alpha is None else alpha

        # update the value estimates with the current reward
        q_n = qn_per_action[action]
        qn_per_action[action] = q_n + alpha_val * (curr_reward - q_n)

        actions_taken.append(action)
        rewards_received.append(curr_reward)

    return actions_taken, rewards_received, true_action_vals


def run_ten_armed_testbed(n_runs, n_steps, eps, alpha=None):
    actions = []
    rewards = []
    true_action_values = []
    for _ in tqdm(range(n_runs), desc=f'Running for epsilon = {eps}'):
        a, r, tav = run_nonstationary_k_arm_bandit(n_steps=n_steps, n_arms=10, eps=eps, alpha=alpha)
        actions.append(a)
        rewards.append(r)
        true_action_values.append(tav)
    actions = np.stack(actions)
    rewards = np.stack(rewards)
    true_action_values = np.stack(true_action_values)
    return actions, rewards, true_action_values


def main(n_runs=2000, n_steps=10000):
    # run the experiments (stationary vs nonstationary)
    actions_s, rewards_s, true_values_s = run_ten_armed_testbed(n_runs, n_steps, eps=0.1, alpha=None)
    actions_n, rewards_n, true_values_n = run_ten_armed_testbed(n_runs, n_steps, eps=0.1, alpha=0.1)

    fig, (ax1, ax2) = plt.subplots(2, 1)

    # first plot: average reward over time
    mean_reward_per_step_s = rewards_s.mean(axis=0)
    mean_reward_per_step_n = rewards_n.mean(axis=0)
    ax1.plot(range(n_steps), mean_reward_per_step_s, label='Stationary (a=1/n)')
    ax1.plot(range(n_steps), mean_reward_per_step_n, label='Nonstationary (a=0.1)')
    ax1.set_xlabel('Steps')
    ax1.set_ylabel('Average reward')

    # second plot: optimal actions per step
    optimal_actions_s = true_values_s.argmax(axis=1).reshape(-1, 1)
    optimal_actions_n = true_values_n.argmax(axis=1).reshape(-1, 1)

    percent_optimal_actions_0 = (actions_s == optimal_actions_s).sum(axis=0) / actions_s.shape[0]
    percent_optimal_actions_1p = (actions_n == optimal_actions_n).sum(axis=0) / actions_n.shape[0]

    ax2.plot(range(n_steps), percent_optimal_actions_0, label='Sample-average (a=1/n)')
    ax2.plot(range(n_steps), percent_optimal_actions_1p, label='Constant step size (a=0.1)')
    ax2.set_xlabel('Steps')
    ax2.set_ylabel('% Optimal action')

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
