import pygame
from utils.pathFind import Node
import heapq


def aStar(maze, DIRECTS=None):
    queue = []
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
        queue.append(curNode)


        if curNode == endNode:
            path = []
            tmp = curNode
            while tmp:
                path.append(tmp.pos)
                tmp = tmp.parent
            return queue, path

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

pygame.init()

window = pygame.display.set_mode((1280,720))

clock = pygame.time.Clock()

from utils.maze import mazeGenerate, printMaze
maze = mazeGenerate(48,27)

BOXSIZE = 13

def drawMaze(maze, boxSize):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            colors = {0:(100,100,100),
                      1:(0,0,0),
                      2:(255,255,255)}
            color = colors[maze[r][c]]
            pygame.draw.rect(window, color,
                             (r*boxSize,c*boxSize,boxSize,boxSize))

drawMaze(maze, BOXSIZE)
import time
t = time.time()
queue, path = aStar(maze)
print(time.time()-t)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
    while queue:
        q = queue.pop(0)
        pygame.draw.rect(window, (255,0,0),
                         (q.pos[0]*BOXSIZE,q.pos[1]*BOXSIZE,BOXSIZE,BOXSIZE ))
        pygame.display.flip()
        clock.tick(120)


    clock.tick(20)

