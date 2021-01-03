import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import dijkstra

from generate_maze import MazeGenerator


def get_maze_adjacency(maze):
    nodes = list(zip(*np.where(maze == 0)))
    node_to_idx = {n: i for i, n in enumerate(nodes)}

    # create the adjacency matrix of the path cells
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


def dijkstra_shortest_path(adjacency_matrix, start_node_idx, target_node_idx):
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
    nodes, adjacency = get_maze_adjacency(maze)
    path = dijkstra_shortest_path(adjacency, start_node_idx=0, target_node_idx=len(nodes)-1)
    return [nodes[i] for i in path]


def show_maze_path(maze, path):
    # change the pixel values to create an image
    maze = np.where(maze == 0, 255, 0)
    maze = np.tile(maze.reshape((1, *maze.shape)), [3, 1, 1])

    # draw the path on the maze
    for y, x in path:
        maze[2, y, x] = 0

    maze = maze.transpose((1, 2, 0))
    plt.imshow(maze)
    plt.axis('off')
    plt.show()
    return


if __name__ == '__main__':
    GRID_HEIGHT = 100
    GRID_WIDTH = 200

    create_maze = MazeGenerator()
    m = create_maze(GRID_HEIGHT, GRID_WIDTH)
    solution = dijkstra_solution(m)

    show_maze_path(m, solution)
