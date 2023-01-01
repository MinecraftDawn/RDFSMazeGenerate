import random
ROW = 20
COL = 20
maze = [[[1, 0] for _ in range(COL)] for _ in range(ROW)]

INIT_X, INIT_Y = 0, 0
END_X, END_Y = COL-1, ROW-1


DIRECTS = [[0, 1], # right
          [1, 0], # down
          [-1, 0], # up
          [0, -1]] # left

def rdfs(x, y):
    maze[x][y][0] = 0
    candidates = []
    for i in range(len(DIRECTS)):
        DIR = DIRECTS[i]
        nx, ny = x + DIR[0], y + DIR[1]
        if nx < 0 or nx >= COL or ny < 0 or ny >= ROW:
            continue
        candidates.append(DIR)

    if not candidates: return
    random.shuffle(candidates)

    for DIR in candidates:
        nx, ny = x + DIR[0], y + DIR[1]
        if maze[nx][ny][0] == 0: continue

        if DIR == [0, 1]:
            maze[x][y][1] += 1
        elif DIR == [1, 0]:
            maze[x][y][1] += 2
        elif DIR == [-1, 0]:
            maze[x][y][1] += 4
        elif DIR == [0, -1]:
            maze[x][y][1] += 8

        rdfs(nx, ny)


rdfs(0, 0)

def printMaze():
    out = [[1 for c in range(COL*2+1)] for r in range(ROW*2+1)]

    for r in range(len(maze)):
        for c in range(len(maze[0])):
            row, col = r*2+1, c*2+1
            out[row][col] = 0
            if maze[r][c][1] >= 8:
                maze[r][c][1] -= 8
                out[row][col-1] = 0
            if maze[r][c][1] >= 4:
                maze[r][c][1] -= 4
                out[row-1][col] = 0
            if maze[r][c][1] >= 2:
                maze[r][c][1] -= 2
                out[row+1][col] = 0
            if maze[r][c][1] >= 1:
                maze[r][c][1] -= 1
                out[row][col+1] = 0

    for r in range(len(out)):
        for c in range(len(out[0])):
            if out[r][c]:
                print('##', end='')
            else:
                print('  ', end='')
        print()

printMaze()

for r in range(ROW):
    for c in range(COL):
        print(maze[r][c], end='')
    print()
