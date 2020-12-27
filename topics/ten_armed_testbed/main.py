"""Run 2000 10-arm bandit problems with the sample-average action-value method"""

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm


def run_k_arm_bandit(n_steps, n_arms, eps):
    reward_total_per_action = np.zeros(n_arms)
    action_counts = np.zeros(n_arms)

    # sample the true q* value per action from a unit Gaussian
    true_action_vals = np.random.randn(n_arms)

    # sample the rewards per action for each step
    # resulting array will have shape (n_steps, n_arms)
    sample_rewards = np.stack([np.random.normal(q_a, 1, n_steps) for q_a in true_action_vals]).T

    actions_taken = []
    rewards_received = []
    values = np.zeros(n_arms)
    for rewards in sample_rewards:
        if np.random.rand() < eps:  # exploration: choose random action with probability `eps`
            action = np.random.randint(0, n_arms)
        else:  # exploitation: select the action with the highest current estimated value
            action = values.argmax()
        curr_reward = rewards[action]

        actions_taken.append(action)
        rewards_received.append(curr_reward)

        # update the value estimates with the current reward
        reward_total_per_action[action] += curr_reward
        action_counts[action] += 1
        nonzero_mask = (action_counts != 0)
        values[nonzero_mask] = reward_total_per_action[nonzero_mask] / action_counts[nonzero_mask]

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
