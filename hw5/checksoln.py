import numpy as np
import sys

# check command line parameters
if len(sys.argv) < 3:
    print('Usage:')
    print('    python3 checksoln.py [maze file] [solution file]')
    sys.exit(0)

# extra command line parameters
maze_file = sys.argv[1]
solution_file = sys.argv[2]

# read maze file to a 2-d np boolean array maze
with open(maze_file, "r") as f:
    size = f.readline().strip().split()
    max_row = int(size[0])
    max_col = int(size[1])
    maze = np.zeros((max_row, max_col), dtype=bool)
    for line in f.readlines():
        wall = line.strip().split()
        maze[int(wall[0])][int(wall[1])] = 1

# read solution file to a list path
with open(solution_file, "r") as f:
    path = []
    for line in f.readlines():
        cell = line.strip().split()
        path.append((int(cell[0]), int(cell[1])))

# check if extrance and exit are valid
if path[0][0] != 0 or maze[0][path[0][1]] == 1 or path[len(path) - 1][0] != max_row - 1:
    print("Solution is invalid for getting a wrong entrance or exit!")
    sys.exit(0)

# check if each step is valid
for i in range(1, len(path)):
    # initialize flag as valid
    valid = True
    row = path[i][0]
    col = path[i][1]
    if row < 0 or row >= max_row or col < 0 or col >= max_col:
        valid = False
    if maze[row][col] == 1:
        valid = False
    # check if each step moves exactly one position
    if np.abs(row - path[i - 1][0]) + np.abs(col - path[i - 1][1]) != 1:
        valid = False
    # indicate invalid solution if any one checking fails
    if not valid:
        print("Solution is invalid for invalid position change!")
        sys.exit(0)

# indicate valid solution if no invalid conditions found
print("Solution is valid!")
