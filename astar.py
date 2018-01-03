__author__ = 'Unomi'
import math

class Tile:
    def __init__(self, list_of_coords):
        self.x = list_of_coords[0]
        self.y = list_of_coords[1]
        self.z = list_of_coords[2]

    def distance(self, other):
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def neighbours(self, width, length, height):
        coords = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                # for z in range(-1, 2):
                z = 0
                if x != 0 or y != 0 or z != 0:
                    if 0 <= self.x + x <= width and 0 <= self.y + y <= length and 0 <= self.z + z <= height:
                        coords.append([self.x + x, self.y + y, self.z + z])
        return coords

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __str__(self):
        return str(self.x) + ':' + str(self.y) + ':' + str(self.z)


class Node:
    def __init__(self, point, fscore=float('inf'), gscore=float('inf'), cameFrom=None):
        self.point = point
        self.fscore = fscore
        self.gscore = gscore
        self.cameFrom = cameFrom


def append_to_set(set_of_nodes, node):
    i = 0
    for i in range(len(set_of_nodes)):
        if set_of_nodes[i].fscore <= node.fscore:
            break

    set_of_nodes.insert(i, node)


def drawRect(ix, iy, color='white'):
    # mySquare = Rectangle(Point(ix*10, iy*10), Point(ix*10+9, iy*10+9))
    # mySquare.setFill(color)
    # mySquare.draw(win)
    pass

def astar(start, goal):
    start = Node(Tile(start))
    goal = Node(Tile(goal))
    start.fscore = start.point.distance(goal.point)
    start.gscore = 0
    openSet = [start]
    closedSet = {
        str(Tile([6, 6, 0])): True,
        str(Tile([6, 5, 0])): True,
        str(Tile([5, 6, 0])): True,
        str(Tile([4, 6, 0])): True,
        str(Tile([6, 4, 0])): True,
        str(Tile([6, 3, 0])): True,
        str(Tile([3, 6, 0])): True,
        }
    openSetDict = {str(start.point): True}

    for ix in range(50):
        for iy in range(50):
            drawRect(ix, iy)

    current = None

    while len(openSet) > 0:
        #mySquare = Rectangle(Point(1, 1), Point(9, 9))
        if current:
            drawRect(current.point.x, current.point.y, 'gray')
        current = openSet.pop()
        drawRect(current.point.x, current.point.y, 'green')
        del openSetDict[str(current.point)]

        if current.point == goal.point:
            return reconstruct_path(current)

        closedSet[str(current.point)] = True
        # print(len(closedSet), len(openSetDict), len(openSet))

        for coords in current.point.neighbours(50, 50, 0):
            neighbor = Node(Tile(coords))
            if not closedSet.get(str(Tile(coords)), False) and not openSetDict.get(str(Tile(coords)), False):
                append_to_set(openSet, neighbor)
                openSetDict[str(neighbor.point)] = True
                drawRect(current.point.x, current.point.y, 'red')

            tentative_gScore = current.gscore + current.point.distance(neighbor.point)
            if tentative_gScore >= neighbor.gscore:
                continue

            neighbor.cameFrom = current
            neighbor.gscore = tentative_gScore
            neighbor.fscore = neighbor.gscore + neighbor.point.distance(goal.point)

    return None


def reconstruct_path(current):
    total_path = [current]
    while current.cameFrom:
        current = current.cameFrom
        total_path.append(current)
    return total_path


tot = astar([0, 0, 0], [49, 49, 0])