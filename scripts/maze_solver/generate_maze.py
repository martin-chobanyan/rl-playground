import random

import matplotlib.pyplot as plt
import numpy as np


def surrounding_cells(rand_wall, val=0):
    count = 0
    for y_diff, x_diff in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        if maze[rand_wall[0] + y_diff, rand_wall[1] + x_diff] == val:
            count += 1
    return count


def leftmost_cell(maze, walls, x, y, wall_val=1):
    if x != 0:
        if maze[y, x - 1] != 0:
            maze[y, x - 1] = wall_val
        if [y, x - 1] not in walls:
            walls.append([y, x - 1])


def rightmost_cell(maze, walls, x, y, wall_val=1):
    _, grid_width = maze.shape
    if x != grid_width - 1:
        if maze[y, x + 1] != 0:
            maze[y, x + 1] = wall_val
        if [y, x + 1] not in walls:
            walls.append([y, x + 1])


def uppermost_cell(maze, walls, x, y, wall_val=1):
    if y != 0:
        if maze[y - 1, x] != 0:
            maze[y - 1, x] = wall_val
        if [y - 1, x] not in walls:
            walls.append([y - 1, x])


def bottommost_cell(maze, walls, x, y, wall_val=1):
    if y != GRID_HEIGHT - 1:
        if maze[y + 1, x] != 0:
            maze[y + 1, x] = wall_val
        if [y + 1, x] not in walls:
            walls.append([y + 1, x])


wall = 1
cell = 0
unvisited = -1

GRID_HEIGHT = 20
GRID_WIDTH = 40
maze = np.full((GRID_HEIGHT, GRID_WIDTH), -1)

# Randomize starting point and set it a cell
start_y = np.random.randint(1, GRID_HEIGHT - 1)
start_x = np.random.randint(1, GRID_WIDTH - 1)

# Mark it as cell and add surrounding walls to the list
maze[start_y, start_x] = cell
walls = [
    [start_y - 1, start_x],
    [start_y, start_x - 1],
    [start_y, start_x + 1],
    [start_y + 1, start_x]
]
for y_wall, x_wall in walls:
    maze[y_wall, x_wall] = wall

while walls:
    random_wall = random.choice(walls)
    y_wall, x_wall = random_wall

    # Check if it is a left wall
    if x_wall != 0:
        if maze[y_wall, x_wall - 1] == -1 and maze[y_wall, x_wall + 1] == 0:
            if surrounding_cells(random_wall) < 2:
                # Denote the new path
                maze[y_wall, x_wall] = 0

                # Mark the new walls
                uppermost_cell(maze, walls, x_wall, y_wall)
                bottommost_cell(maze, walls, x_wall, y_wall)
                leftmost_cell(maze, walls, x_wall, y_wall)

            walls.remove(random_wall)
            continue

    # Check if it is an upper wall
    if y_wall != 0:
        if maze[y_wall - 1, x_wall] == -1 and maze[y_wall + 1, x_wall] == 0:
            if surrounding_cells(random_wall) < 2:
                # Denote the new path
                maze[y_wall, x_wall] = 0

                # Mark the new walls
                uppermost_cell(maze, walls, x_wall, y_wall)
                leftmost_cell(maze, walls, x_wall, y_wall)
                rightmost_cell(maze, walls, x_wall, y_wall)

            walls.remove(random_wall)
            continue

    # Check the bottom wall
    if y_wall != GRID_HEIGHT - 1:
        if maze[y_wall + 1, x_wall] == -1 and maze[y_wall - 1, x_wall] == 0:
            if surrounding_cells(random_wall) < 2:
                # Denote the new path
                maze[y_wall, x_wall] = 0

                # Mark the new walls
                leftmost_cell(maze, walls, x_wall, y_wall)
                rightmost_cell(maze, walls, x_wall, y_wall)
                bottommost_cell(maze, walls, x_wall, y_wall)

            walls.remove(random_wall)
            continue

    # Check the right wall
    if x_wall != GRID_WIDTH - 1:
        if maze[y_wall, x_wall + 1] == -1 and maze[y_wall, x_wall - 1] == 0:
            if surrounding_cells(random_wall) < 2:
                # Denote the new path
                maze[y_wall, x_wall] = 0

                # Mark the new walls
                rightmost_cell(maze, walls, x_wall, y_wall)
                bottommost_cell(maze, walls, x_wall, y_wall)
                uppermost_cell(maze, walls, x_wall, y_wall)

            walls.remove(random_wall)
            continue

    walls.remove(random_wall)

# Mark the remaining unvisited cells as walls
maze[maze == -1] = 1

# Set entrance and exit
x_entrance = np.where(maze[1, :] == 0)[0][0]  # x-coord of the first open cell in the second row
x_exit = np.where(maze[-2, :] == 0)[0][-1]    # x-coord of the first open cell in the penultimate row
maze[0, x_entrance] = 0
maze[-1, x_exit] = 0

maze = np.where(maze == 0, 1, 0)
plt.imshow(maze, cmap='gray')
plt.axis('off')
plt.show()
