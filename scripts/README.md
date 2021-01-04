# Reinforcement Learning Topics

This directory contains python scripts for various topics in reinforcement learning, 
primarily from the "Reinforcement Learning: An Introduction 2nd Edition" by Sutton et al. 

### 10-armed Testbed
This script recreates Figure 2.2 in Section 2.3 by executing 2000 independent runs 
using the sample-average action-value method with three different settings (greedy, epsilon=0.01, and epsilon=0.1)



### Maze Solver

This contains code for generating a random maze using Prim's algorithm, solving the maze using Dijkstra's shortest path algorithm, and solving the maze using value iteration with dynamic programming.

The reason for having both a Dijkstra solution and a reinforcement learning solution is to serve as a sanity check and make sure that the both solutions output the shortest path solution.