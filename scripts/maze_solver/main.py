"""A demo example for both the Dijkstra and Value Iteration solutions to a random maze"""

import matplotlib.pyplot as plt

from dijkstra import dijkstra_solution
from generate_maze import MazeGenerator
from maze_utils import plot_maze
from value_iter import MazeEnvironment, value_iteration_solution

if __name__ == '__main__':
    # create the maze
    GRID_HEIGHT = 40
    GRID_WIDTH = 40
    create_maze = MazeGenerator()
    maze = create_maze(GRID_HEIGHT, GRID_WIDTH)

    # gather both solutions
    d_solution = dijkstra_solution(maze)
    v_solution, *_ = value_iteration_solution(MazeEnvironment(maze))

    # plot the solutions
    fig, (ax1, ax2) = plt.subplots(1, 2)
    ax1 = plot_maze(ax1, maze, d_solution)
    ax2 = plot_maze(ax2, maze, v_solution)
    ax1.set_title('Dijkstra Solution')
    ax2.set_title('Value Iteration Solution')
    plt.show()
