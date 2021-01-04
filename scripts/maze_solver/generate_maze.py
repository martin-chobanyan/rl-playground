"""This script defines a class for generating random mazes using Prim's algorithm"""

import random

import matplotlib.pyplot as plt
import numpy as np

WALL = 1
PATH = 0
UNVISITED = -1

GRID_HEIGHT = 20
GRID_WIDTH = 40


class MazeGenerator:
    """Generate a random maze using Prim's algorithm"""
    def __init__(self):
        self.maze = None
        self.grid_width = None
        self.grid_height = None
        self._walls = None

    def reset_maze(self, grid_height, grid_width):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.maze = np.full((self.grid_height, self.grid_width), UNVISITED)
        self._walls = []

    def surrounding_path_cells(self, cell):
        count = 0
        for y_diff, x_diff in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self.maze[cell[0] + y_diff, cell[1] + x_diff] == PATH:
                count += 1
        return count

    def check_left_cell(self, x, y):
        try:
            if self.maze[y, x - 1] != PATH:
                self.maze[y, x - 1] = WALL
            if [y, x - 1] not in self._walls:
                self._walls.append([y, x - 1])
        except IndexError:
            pass

    def check_right_cell(self, x, y):
        try:
            if self.maze[y, x + 1] != PATH:
                self.maze[y, x + 1] = WALL
            if [y, x + 1] not in self._walls:
                self._walls.append([y, x + 1])
        except IndexError:
            pass

    def check_top_cell(self, x, y):
        try:
            if self.maze[y - 1, x] != PATH:
                self.maze[y - 1, x] = WALL
            if [y - 1, x] not in self._walls:
                self._walls.append([y - 1, x])
        except IndexError:
            pass

    def check_bottom_cell(self, x, y):
        try:
            if self.maze[y + 1, x] != PATH:
                self.maze[y + 1, x] = WALL
            if [y + 1, x] not in self._walls:
                self._walls.append([y + 1, x])
        except IndexError:
            pass

    def __call__(self, grid_height, grid_width):
        self.reset_maze(grid_height, grid_width)

        # random starting point
        start_y = np.random.randint(1, self.grid_height - 1)
        start_x = np.random.randint(1, self.grid_width - 1)

        # mark it as a path cell and add the neighboring cells as walls
        self.maze[start_y, start_x] = PATH

        # add the cells surrounding the selected start cell
        self._walls += [
            [start_y - 1, start_x],
            [start_y, start_x - 1],
            [start_y, start_x + 1],
            [start_y + 1, start_x]
        ]

        for y_wall, x_wall in self._walls:
            self.maze[y_wall, x_wall] = WALL

        while len(self._walls) > 0:
            random_wall = random.choice(self._walls)
            y_wall, x_wall = random_wall

            # left wall
            if x_wall != 0:
                if self.maze[y_wall, x_wall - 1] == UNVISITED and self.maze[y_wall, x_wall + 1] == PATH:
                    if self.surrounding_path_cells(random_wall) < 2:
                        self.maze[y_wall, x_wall] = PATH
                        self.check_left_cell(x_wall, y_wall)
                        self.check_top_cell(x_wall, y_wall)
                        self.check_bottom_cell(x_wall, y_wall)
                    self._walls.remove(random_wall)
                    continue

            # top wall
            if y_wall != 0:
                if self.maze[y_wall - 1, x_wall] == UNVISITED and self.maze[y_wall + 1, x_wall] == PATH:
                    if self.surrounding_path_cells(random_wall) < 2:
                        self.maze[y_wall, x_wall] = PATH
                        self.check_top_cell(x_wall, y_wall)
                        self.check_left_cell(x_wall, y_wall)
                        self.check_right_cell(x_wall, y_wall)
                    self._walls.remove(random_wall)
                    continue

            # bottom wall
            if y_wall != self.grid_height - 1:
                if self.maze[y_wall + 1, x_wall] == UNVISITED and self.maze[y_wall - 1, x_wall] == PATH:
                    if self.surrounding_path_cells(random_wall) < 2:
                        self.maze[y_wall, x_wall] = PATH
                        self.check_bottom_cell(x_wall, y_wall)
                        self.check_left_cell(x_wall, y_wall)
                        self.check_right_cell(x_wall, y_wall)
                    self._walls.remove(random_wall)
                    continue

            # right wall
            if x_wall != self.grid_width - 1:
                if self.maze[y_wall, x_wall + 1] == UNVISITED and self.maze[y_wall, x_wall - 1] == PATH:
                    if self.surrounding_path_cells(random_wall) < 2:
                        self.maze[y_wall, x_wall] = PATH
                        self.check_right_cell(x_wall, y_wall)
                        self.check_bottom_cell(x_wall, y_wall)
                        self.check_top_cell(x_wall, y_wall)
                    self._walls.remove(random_wall)
                    continue
            self._walls.remove(random_wall)

        # ensure all unvisited cells are transformed into wall cells
        self.maze[self.maze == UNVISITED] = WALL

        # set the entrance and exit cells
        x_enter = np.where(self.maze[1, :] == PATH)[0][0]  # x-coord of first open cell in second row
        x_exit = np.where(self.maze[-2, :] == PATH)[0][-1]  # x-coord of last open cell in penultimate row
        self.maze[0, x_enter] = PATH
        self.maze[-1, x_exit] = PATH

        return self.maze


if __name__ == '__main__':
    create_maze = MazeGenerator()
    m = create_maze(50, 100)
    m = np.where(m == 0, 1, 0)
    plt.imshow(m, cmap='gray')
    plt.axis('off')
    plt.show()
