"""Value iteration solution to a maze

States
------
Number of open/path cells

Actions
-------
Left, Up, Right, Down

Rewards
-------
-1 for all state transitions except the terminal state (0 reward)

Notes
-----
* p(s', r | s, a) = 0 or 1 for all states and actions (deterministic environment dynamics)
* Episodic -> no discount, penalize the length of the solution
* Value Iteration update: V(s) <- max(reward + V(s'))
* Optimal Policy update: pi(s) = argmax over actions (reward + V(s'))
"""

import matplotlib.pyplot as plt
import numpy as np

from generate_maze import MazeGenerator
from maze_utils import index_maze_cells, plot_maze

# constant action IDs
LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

ACTIONS = [LEFT, UP, RIGHT, DOWN]


class MazeEnvironment:
    """Wrapper class around a maze which facilitates interactions

    Parameters
    ----------
    maze: numpy.ndarray
        A 2D numpy array where 0 = open cell, 1 = wall
    """
    def __init__(self, maze):
        self.maze = maze

        self.open_cells, self.cell_to_index = index_maze_cells(self.maze)

        # isolate the terminal state in the last row
        self.goal = (self.maze.shape[0] - 1, np.where(self.maze[-1] == 0)[0][-1])

        self.action_increments = {
            LEFT: (0, -1),
            UP: (-1, 0),
            RIGHT: (0, 1),
            DOWN: (1, 0)
        }

    def transition(self, cell, action):
        """Perform a state transition in the maze

        Parameters
        ----------
        cell: tuple
            The (y, x) tuple for the current cell in the maze
        action: int
            One of four actions (left, up, right, down)

        Returns
        -------
        tuple, float
            The next cell/state along with the reward
        """
        y, x = cell
        assert self.maze[y, x] == 0, 'Input is not an open path cell!'
        assert action in self.action_increments, 'Unknown action!'

        if cell == self.goal:
            return cell, 0

        y_diff, x_diff = self.action_increments[action]
        y_new = y + y_diff
        x_new = x + x_diff

        try:
            cell_val = self.maze[y_new, x_new]
        except IndexError:
            pass
        else:
            if cell_val == 0:
                return (y_new, x_new), -1
        return cell, -1


def calculate_action_values(maze_env, cell, values):
    """Calculate the action-values given the maze environment, current cell, and current value function

    Parameters
    ----------
    maze_env: MazeEnvironment
    cell: tuple
    values: numpy.ndarray

    Returns
    -------
    list[float]
    """
    action_values = []
    for action in ACTIONS:
        new_cell, reward = maze_env.transition(cell, action)
        v = values[maze_env.cell_to_index[new_cell]]  # value of next state
        action_values.append(reward + v)
    return action_values


def value_iteration_solution(maze_env, value_threshold=1e-5):
    """Value Iteration approach to solving a maze

    Parameters
    ----------
    maze_env: MazeEnvironment
    value_threshold: float, optional

    Returns
    -------
    dict[tuple, int], list[tuple]
    """
    num_states = len(maze_env.open_cells)
    values = np.zeros(num_states)

    # value iteration: approximate the value function
    value_change = 1
    while value_change > value_threshold:
        value_change = 0
        old_values = values.copy()
        for i, cell in enumerate(maze_env.open_cells):
            action_values = calculate_action_values(maze_env, cell, values)
            values[i] = max(action_values)
        value_change = max(value_change, np.abs(values - old_values).max())

    # defining the policy: map a cell to one of four actions
    policy = dict()
    for cell in maze_env.open_cells:
        action_values = np.array(calculate_action_values(maze_env, cell, values))
        policy[cell] = ACTIONS[action_values.argmax()]

    # apply the policy
    current_cell = maze_env.open_cells[0]
    maze_solution = [current_cell]
    while current_cell != maze_env.goal:
        current_cell, _ = maze_env.transition(current_cell, policy[current_cell])
        maze_solution.append(current_cell)
    return maze_solution, policy, values


if __name__ == '__main__':
    GRID_HEIGHT = 40
    GRID_WIDTH = 80

    create_maze = MazeGenerator()
    m = create_maze(GRID_HEIGHT, GRID_WIDTH)
    env = MazeEnvironment(m)

    path, *_ = value_iteration_solution(env)

    fig, ax = plt.subplots()
    plot_maze(ax, m, path)
    plt.show()
