ROW = 20
COL = 20
MAZE = [[[1, 0] for _ in range(COL)] for _ in range(ROW)]

INIT_X, INIT_Y = 0, 0
END_X, END_Y = COL-1, ROW-1


DIRECTS = [[0, 1], # right
          [1, 0], # down
          [-1, 0], # up
          [0, -1]] # left


from utils.maze import mazeGenerate, printMaze
from utils.pathFind import aStar, bfs


maze = mazeGenerate()

# maze = bfs(maze)
path = aStar(maze)
for pos in path:
    r,c = pos
    maze[r][c] = 2
printMaze(maze)
