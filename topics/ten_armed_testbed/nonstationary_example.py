"""Run the modified ten-armed bandit testbed as specified in exercise 2.5"""

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


def run_k_arm_bandit(n_steps, n_arms, eps, alpha=None):
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

    # sample the rewards per action for each step
    # resulting array will have shape (n_steps, n_arms)
    sample_rewards = np.stack([np.random.normal(q_a, 1, n_steps) for q_a in true_action_vals]).T

    actions_taken = []
    rewards_received = []
    for rewards in sample_rewards:
        # exploration: choose random action with probability `eps`
        if np.random.rand() < eps:
            action = np.random.randint(0, n_arms)
        # exploitation: select the action with the highest current estimated value
        else:
            action = qn_per_action.argmax()
        curr_reward = rewards[action]

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


def run_ten_armed_testbed(n_runs, n_steps, eps):
    actions = []
    rewards = []
    true_action_values = []
    for _ in tqdm(range(n_runs), desc=f'Running for epsilon = {eps}'):
        a, r, tav = run_k_arm_bandit(n_steps=n_steps, n_arms=10, eps=eps)
        actions.append(a)
        rewards.append(r)
        true_action_values.append(tav)
    actions = np.stack(actions)
    rewards = np.stack(rewards)
    true_action_values = np.stack(true_action_values)
    return actions, rewards, true_action_values


def main(n_runs=2000, n_steps=1000):
    # run the experiments
    actions_0, rewards_0, true_values_0 = run_ten_armed_testbed(n_runs, n_steps, 0)
    actions_1p, rewards_1p, true_values_1p = run_ten_armed_testbed(n_runs, n_steps, 0.01)
    actions_10p, rewards_10p, true_values_10p = run_ten_armed_testbed(n_runs, n_steps, 0.1)

    fig, (ax1, ax2) = plt.subplots(2, 1)

    # first plot: average reward over time
    mean_reward_per_step_0 = rewards_0.mean(axis=0)
    mean_reward_per_step_1p = rewards_1p.mean(axis=0)
    mean_reward_per_step_10p = rewards_10p.mean(axis=0)
    ax1.plot(range(n_steps), mean_reward_per_step_0, color='green', label='Eps=0 (greedy)')
    ax1.plot(range(n_steps), mean_reward_per_step_1p, color='red', label='Eps=0.01')
    ax1.plot(range(n_steps), mean_reward_per_step_10p, color='blue', label='Eps=0.1')
    ax1.set_xlabel('Steps')
    ax1.set_ylabel('Average reward')

    # second plot: optimal actions per step
    optimal_actions_0 = true_values_0.argmax(axis=1).reshape(-1, 1)
    optimal_actions_1p = true_values_1p.argmax(axis=1).reshape(-1, 1)
    optimal_actions_10p = true_values_10p.argmax(axis=1).reshape(-1, 1)

    percent_optimal_actions_0 = (actions_0 == optimal_actions_0).sum(axis=0) / actions_0.shape[0]
    percent_optimal_actions_1p = (actions_1p == optimal_actions_1p).sum(axis=0) / actions_1p.shape[0]
    percent_optimal_actions_10p = (actions_10p == optimal_actions_10p).sum(axis=0) / actions_10p.shape[0]

    ax2.plot(range(n_steps), percent_optimal_actions_0, color='green', label='Eps=0 (greedy)')
    ax2.plot(range(n_steps), percent_optimal_actions_1p, color='red', label='Eps=0.01')
    ax2.plot(range(n_steps), percent_optimal_actions_10p, color='blue', label='Eps=0.1')
    ax2.set_xlabel('Steps')
    ax2.set_ylabel('% Optimal action')

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
