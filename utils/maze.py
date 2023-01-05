import random


def rdfs(r, c, roads, DIRECTS):
    roads[r][c][0] = 0
    candidates = []
    ROW, COL = len(roads), len(roads[0])
    for i in range(len(DIRECTS)):
        DIR = DIRECTS[i]
        nr, nc = r + DIR[0], c + DIR[1]
        if nc < 0 or nc >= COL or nr < 0 or nr >= ROW:
            continue
        candidates.append(DIR)

    if not candidates: return
    random.shuffle(candidates)

    for DIR in candidates:
        nr, nc = r + DIR[0], c + DIR[1]
        if roads[nr][nc][0] == 0: continue

        if DIR == [0, 1]:
            roads[r][c][1] += 1
        elif DIR == [1, 0]:
            roads[r][c][1] += 2
        elif DIR == [-1, 0]:
            roads[r][c][1] += 4
        elif DIR == [0, -1]:
            roads[r][c][1] += 8

        rdfs(nr, nc, roads, DIRECTS)

def mazeBuilder(roads):
    ROW, COL = len(roads), len(roads[0])
    out = [[1 for _ in range(COL*2+1)] for _ in range(ROW*2+1)]

    for r in range(len(roads)):
        for c in range(len(roads[0])):
            row, col = r*2+1, c*2+1
            out[row][col] = 0
            if roads[r][c][1] >= 8:
                roads[r][c][1] -= 8
                out[row][col-1] = 0
            if roads[r][c][1] >= 4:
                roads[r][c][1] -= 4
                out[row-1][col] = 0
            if roads[r][c][1] >= 2:
                roads[r][c][1] -= 2
                out[row+1][col] = 0
            if roads[r][c][1] >= 1:
                roads[r][c][1] -= 1
                out[row][col+1] = 0
    return out

def mazeGenerate(ROW=10, COL=10, DIRECTS=None):
    ROADS = [[[1, 0] for _ in range(COL)] for _ in range(ROW)]
    INIT_X, INIT_Y = 0, 0

    if not DIRECTS:
        DIRECTS = [[0, 1], # right
                  [1, 0], # down
                  [-1, 0], # up
                  [0, -1]] # left

    rdfs(INIT_X, INIT_Y, ROADS, DIRECTS)

    maze = mazeBuilder(ROADS)
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