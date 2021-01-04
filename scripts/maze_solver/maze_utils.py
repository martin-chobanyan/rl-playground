"""Utilities for solving a maze"""

import numpy as np


def index_maze_cells(maze):
    """Index the open cells in the maze

    Parameters
    ----------
    maze: numpy.ndarray
        A 2D numpy array where 0 = open cell, 1 = wall

    Returns
    -------
    list, dict
        A list of the open cell (y, x) coordinates and a dictionary mapping each coordinate to its index
    """
    nodes = list(zip(*np.where(maze == 0)))
    node_to_idx = {n: i for i, n in enumerate(nodes)}
    return nodes, node_to_idx


def get_maze_adjacency(maze):
    """Create an adjacency matrix defining the connections between open cells

    Parameters
    ----------
    maze: numpy.ndarray
        A 2D numpy array where 0 = open cell, 1 = wall

    Returns
    -------
    list, numpy.ndarray
        A list of the nodes (open cell coordinates within the maze) and the adjacency matrix as a numpy array
    """
    # create the adjacency matrix of the path cells
    nodes, node_to_idx = index_maze_cells(maze)
    num_nodes = len(nodes)
    adjacency = np.zeros((num_nodes, num_nodes))
    for i, (y, x) in enumerate(nodes):
        for y_diff, x_diff in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            try:
                neighbor = (y + y_diff, x + x_diff)
                adjacency[i, node_to_idx[neighbor]] = 1
            except KeyError:
                pass
    return nodes, adjacency


def plot_maze(ax, maze, path=None, color=(255, 0, 0)):
    """Plot the maze with an optional solution

    Parameters
    ----------
    ax: matplotlib.pyplot.Axes
        The matplotlib axis to plot on
    maze: numpy.ndarray
        A 2D numpy array where 0 = open cell, 1 = wall
    path: list[tuple], optional
        The solution as a list of open cell coordinates. Default is None (i.e. don't plot a solution)
    color: tuple, optional
        The RGB color for the path (default is red)

    Returns
    -------
    matplotlib.pyplot.Axes
    """
    # change the pixel values to create an image
    maze = np.where(maze == 0, 255, 0)
    maze = np.tile(maze.reshape((1, *maze.shape)), [3, 1, 1])

    if path is not None:
        # draw the path on the maze
        for y, x in path:
            maze[:, y, x] = color

    maze = maze.transpose((1, 2, 0))
    ax.imshow(maze)
    ax.axis('off')
    return ax
