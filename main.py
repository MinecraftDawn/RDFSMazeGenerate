import random
from collections import deque
import heapq

ROW = 10
COL = 10
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
        nr, nc = r + DIR[0], c + DIR[1]
        if nc < 0 or nc >= COL or nr < 0 or nr >= ROW:
            continue
        candidates.append(DIR)

    if not candidates: return
    random.shuffle(candidates)

    for DIR in candidates:
        nr, nc = r + DIR[0], c + DIR[1]
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

# for r in range(len(MAZE)):
#     for c in range(len(MAZE[0])):
#         print(MAZE[r][c], end='')
#     print()

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
    queue.append([1, 1])
    visted[1][1] = True
    count = 0
    while queue:
        count += 1
        r, c = queue.popleft()
        visted[r][c] = True
        #if r == len(maze)-2 and c == len(maze[0]) -2: break
        for DIR in DIRECTS:
            R, C = DIR
            nr, nc = r+R, c+C
            if 0 < nr < len(maze) and 0 < nc < len(maze[0]) and maze[nr][nc] == 0 and not visted[nr][nc]:
                queue.append((nr, nc))
                tmp[nr][nc] = DIR.copy()
        if r == len(tmp) - 2 and c == len(tmp[0]) - 2: break

    # for r in range(len(tmp)):
    #     for c in range(len(tmp[0])):
    #         print(tmp[r][c], end='')
    #     print()
    # print(tmp[len(tmp)-2][len(tmp[0])-2])

    print('Count:', count)

    r, c = len(tmp)-2, len(tmp[0])-2
    while tmp[r][c] != [0, 0]:
        maze[r][c] = 2
        dr, dc = tmp[r][c]
        r, c = r-dr, c-dc
    maze[1][1] = 2

    return maze


def evalH(cur, end):
    return abs(cur[0] - end[0]) + abs(cur[1] - end[1])

def evalF(g, h, a=1, b=1):
    return a*g + b*h


class Node():
    def __init__(self, parent=None, pos=None):
        self.parent = parent
        self.pos = pos

        self._g = 0
        self._h = 0

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, g):
        self._g = g

    @property
    def h(self):
        return self._h

    @h.setter
    def h(self, h):
        self._h = h

    @property
    def f(self):
        return self.g + self.h

    def evalH(self, end):
        return abs(self.pos[0] - end[0]) + abs(self.pos[1] - end[1])

    def __eq__(self, other):
        return self.pos == other.pos

def findMinNode(nodes):
    findNode = nodes[0]
    findIndex = 0
    for index, node in enumerate(nodes):
        if node.f < findNode.f:
            findNode = node
            findIndex = index

    return findNode, findIndex

def aStar(maze):
    endR, endC = len(maze)-2, len(maze[0])-2

    startNode = Node(None, (1, 1))
    #start.h = start.evalH((endR,endC))

    endNode = Node(None, (endR, endC))

    open = [startNode]
    close = []

    while open:
        curNode, curIndex = findMinNode(open)

        open.pop(curIndex)
        close.append(curNode)

        if curNode == endNode:
            path = []
            tmp = curNode
            while tmp:
                path.append(tmp.pos)
                tmp = tmp.parent
            return path

        childs = []
        for DIR in DIRECTS:
            R, C = DIR
            nr, nc = curNode.pos[0] + R, curNode.pos[1] + C
            if 0 < nr < len(maze) and 0 < nc < len(maze[0]) and maze[nr][nc] == 0:

                nextNode = Node(curNode, (nr, nc))
                childs.append(nextNode)

        for child in childs:

            if child in close:
                continue

            child.g = curNode.g + 1
            child.h = child.evalH((endR,endC))

            for openNode in open:
                if child == openNode and child.g > openNode.g:
                    continue

            open.append(child)


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

rdfs(0, 0)

maze = generateMaze()

# maze = bfs(maze)
path = aStar(maze)
for pos in path:
    r,c = pos
    maze[r][c] = 2
printMaze(maze)
