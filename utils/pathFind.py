import heapq
from collections import deque

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

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

    def __hash__(self):
        return hash(self.pos)

def aStar(maze, DIRECTS=None):
    endR, endC = len(maze)-2, len(maze[0])-2

    startNode = Node(None, (1, 1))
    endNode = Node(None, (endR, endC))

    if not DIRECTS:
        DIRECTS = [[0, 1], # right
                  [1, 0], # down
                  [-1, 0], # up
                  [0, -1]] # left

    open = [startNode]
    close = set()

    openSet = {startNode}

    while open:
        curNode = heapq.heappop(open)
        openSet.remove(curNode)
        close.add(curNode)


        if curNode == endNode:
            path = []
            tmp = curNode
            while tmp:
                path.append(tmp.pos)
                tmp = tmp.parent
            return path

        for DIR in DIRECTS:
            R, C = DIR
            nr, nc = curNode.pos[0] + R, curNode.pos[1] + C
            if 0 < nr < len(maze) and 0 < nc < len(maze[0]) and maze[nr][nc] == 0:

                nextNode = Node(curNode, (nr, nc))

                if nextNode in close: continue

                nextNode.g = curNode.g + 1
                nextNode.h = nextNode.evalH((endR, endC))

                heapq.heappush(open, nextNode)
                openSet.add(nextNode)

def bfs(maze, DIRECTS=None):
    tmp = [[[0, 0] for _ in range(len(maze[0]))] for _ in range(len(maze))]
    visted = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]

    if not DIRECTS:
        DIRECTS = [[0, 1], # right
                  [1, 0], # down
                  [-1, 0], # up
                  [0, -1]] # left

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

    print('Count:', count)

    r, c = len(tmp)-2, len(tmp[0])-2
    while tmp[r][c] != [0, 0]:
        maze[r][c] = 2
        dr, dc = tmp[r][c]
        r, c = r-dr, c-dc
    maze[1][1] = 2

    return maze