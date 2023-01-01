import random
from collections import deque
ROW = 40
COL = 40
MAZE = [[[1, 0] for _ in range(COL)] for _ in range(ROW)]

INIT_X, INIT_Y = 0, 0
END_X, END_Y = COL-1, ROW-1


DIRECTS = [[0, 1], # right
          [1, 0], # down
          [-1, 0], # up
          [0, -1]] # left

def rdfs(r, c):
    MAZE[r][c][0] = 0
    candidates = []
    for i in range(len(DIRECTS)):
        DIR = DIRECTS[i]
        nc, nr = r + DIR[0], c + DIR[1]
        if nc < 0 or nc >= COL or nr < 0 or nr >= ROW:
            continue
        candidates.append(DIR)

    if not candidates: return
    random.shuffle(candidates)

    for DIR in candidates:
        nc, nr = r + DIR[0], c + DIR[1]
        if MAZE[nr][nc][0] == 0: continue

        if DIR == [0, 1]:
            MAZE[r][c][1] += 1
        elif DIR == [1, 0]:
            MAZE[r][c][1] += 2
        elif DIR == [-1, 0]:
            MAZE[r][c][1] += 4
        elif DIR == [0, -1]:
            MAZE[r][c][1] += 8

        rdfs(nr, nc)


rdfs(0, 0)

def generateMaze():
    out = [[1 for _ in range(COL*2+1)] for _ in range(ROW*2+1)]

    for r in range(len(MAZE)):
        for c in range(len(MAZE[0])):
            row, col = r*2+1, c*2+1
            out[row][col] = 0
            if MAZE[r][c][1] >= 8:
                MAZE[r][c][1] -= 8
                out[row][col-1] = 0
            if MAZE[r][c][1] >= 4:
                MAZE[r][c][1] -= 4
                out[row-1][col] = 0
            if MAZE[r][c][1] >= 2:
                MAZE[r][c][1] -= 2
                out[row+1][col] = 0
            if MAZE[r][c][1] >= 1:
                MAZE[r][c][1] -= 1
                out[row][col+1] = 0

    return out

def bfs(maze):
    tmp = [[[0, 0] for _ in range(len(maze[0]))] for _ in range(len(maze))]
    visted = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]

    queue = deque()
    queue.append((1, 1))
    visted[1][1] = True

    while queue:
        r, c = queue.popleft()
        visted[r][c] = True
        for DIR in DIRECTS:
            R,C = DIR
            nr, nc = r+R, c+C
            if 0 < nr < len(maze) and 0 < nc < len(maze[0]) and maze[nr][nc] == 0 and not visted[nr][nc]:
                queue.append((nr, nc))
                if DIR == [0, 1]:
                    tmp[nr][nc] = [0, 1]
                elif DIR == [1, 0]:
                    tmp[nr][nc] = [1, 0]
                elif DIR == [-1, 0]:
                    tmp[nr][nc] = [-1, 0]
                elif DIR == [0, -1]:
                    tmp[nr][nc] = [0, -1]

    for r in range(len(tmp)):
        for c in range(len(tmp[0])):
            print(tmp[r][c], end='')
        print()
    print(tmp[len(tmp)-2][len(tmp[0])-2])

    r, c = len(tmp)-2, len(tmp[0])-2
    while tmp[r][c] != [0, 0]:
        maze[r][c] = 2
        dr,dc = tmp[r][c]
        r,c = r-dr,c-dc
    maze[1][1] = 2

    return maze


def printMaze(maze):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == 0:
                print('  ', end='')
            elif maze[r][c] == 1:
                print('##', end='')
            elif maze[r][c] == 2:
                print('..', end='')
        print()


maze = generateMaze()

maze = bfs(maze)
printMaze(maze)
