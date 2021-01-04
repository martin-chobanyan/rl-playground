"""A Dijkstra shortest path solution to a maze"""

import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

from generate_maze import MazeGenerator
from maze_utils import get_maze_adjacency, plot_maze


def dijkstra_shortest_path(adjacency_matrix, start_node_idx, target_node_idx):
    """Find the Dijkstra shortest path between two nodes in a graph

    Parameters
    ----------
    adjacency_matrix: numpy.ndarray
    start_node_idx: int
    target_node_idx: int

    Returns
    -------
    list[int]
    """
    graph = csr_matrix(adjacency_matrix)
    _, predecessors = dijkstra(csgraph=graph, directed=True, indices=start_node_idx, return_predecessors=True)

    path = []
    i = target_node_idx
    while i != start_node_idx:
        path.append(i)
        i = predecessors[i]
    path = [start_node_idx] + path[::-1]
    return path


def dijkstra_solution(maze):
    """Solve the maze using Dijkstra's shortest path algorithm"""
    nodes, adjacency = get_maze_adjacency(maze)
    path = dijkstra_shortest_path(adjacency, start_node_idx=0, target_node_idx=len(nodes) - 1)
    return [nodes[i] for i in path]


if __name__ == '__main__':
    GRID_HEIGHT = 20
    GRID_WIDTH = 40
    create_maze = MazeGenerator()
    m = create_maze(GRID_HEIGHT, GRID_WIDTH)
    solution = dijkstra_solution(m)
    fig, ax = plt.subplots()
    plot_maze(ax, m, solution)
    plt.show()
