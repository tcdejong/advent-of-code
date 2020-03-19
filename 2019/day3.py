class Node: 
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def manhattanToOrig(self):
        return abs(self.x) + abs(self.y)

    def isOnEdge(self, edge):
        return edge.x1 <= self.x <= edge.x2 and edge.y1 <= self.y <= edge.y2
        

class Edge:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.x1 = min(start.x, end.x)
        self.x2 = max(start.x, end.x)
        self.y1 = min(start.y, end.y)
        self.y2 = max(start.y, end.y)
        self.vertical = (self.x1 == self.x2)

        self._len = max(self.x2 - self.x1, self.y2 - self.y1)


    def __repr__(self):
        return f"{self.start}=>{self.end}"

    
    def __len__(self):
        return self._len


    def intersection(self, other):
        if not isinstance(other, Edge):
            raise RuntimeError(f"other must be an Edge, but was {type(other)}")

        if self.vertical == other.vertical:
            return None
        
        if self.vertical:
            return other.intersection(self)

        intersectX = other.x1
        intersectY = self.y1

        if not self.x1 < intersectX < self.x2 or not other.y1 < intersectY < other.y2:
            return None

        return Node(intersectX, intersectY)


class Wire:
    def __init__(self, edges):
        self.edges = edges
        self.top = self.right = self.bot = self.left = 0

        for edge in edges:
            self.left = edge.x1 if edge.x1 < self.left else self.left
            self.right = edge.x2 if edge.x2 > self.right else self.right
            self.bot = edge.y1 if edge.y1 < self.bot else self.bot
            self.top = edge.y2 if edge.y2 > self.top else self.top


    def __repr__(self):
        return "".join(str(self.edges))


    def insideBoundingBox(self, edge):
        if edge.vertical:
            return self.left < edge.x1 < self.right and (self.bot < edge.y1 < self.top or self.bot < edge.y2 < self.top)
        else:
            return self.bot < edge.y1 < self.top and (self.left < edge.x1 < self.right or self.left < edge.x2 < self.right)


    def findIntersections(self, other):
        intersections = set()

        myPossibleEdges = [e for e in self.edges if other.insideBoundingBox(e)]
        theirPossibleEdges = [e for e in other.edges if self.insideBoundingBox(e)]

        for myEdge in myPossibleEdges:
            for theirEdge in theirPossibleEdges:
                intersection = myEdge.intersection(theirEdge)
                if intersection:
                    intersections.add(intersection)

        return intersections


    def stepsToTargets(self, targets):
        steps = 0
        stepDict = {}
        
        for edge in self.edges:    
            for target in targets:
                if target.isOnEdge(edge):
                    stepDict[target] = steps + len(Edge(edge.start, target))
            
            steps += len(edge)

        return stepDict

        

def readInput(ex=""):
    """ 
    Read steps from puzzle input or examples, 
    Convert steps to Nodes, 
    Convert nodes to Edges, 
    then return two dictionaries of Edge objects split as vertical and horizontal edges. 
    """

    stepsA = []
    stepsB = []

    if ex == 1:
        stepsA = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(sep=",")
        stepsB = "U62,R66,U55,R34,D71,R55,D58,R83".split(sep=",")
    elif ex == 2:
        stepsA = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(sep=",")
        stepsB = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(sep=",")
    else:
        with open("day3.txt") as rawData:
            stepsA = rawData.readline().strip().split(sep=",")
            stepsB = rawData.readline().strip().split(sep=",")

    nodesA, nodesB = createNodes(stepsA), createNodes(stepsB)
    wireA, wireB = createWire(nodesA), createWire(nodesB)

    return (wireA, wireB)



def createNodes(stepList):
        """ Convert list of instructions to list of sequential Node instances. """
        orig = Node(0, 0)
        nodes = [orig]

        for step in stepList:
            x, y = nodes[-1].x, nodes[-1].y
            dx, dy = 0, 0

            dir = step[:1]
            dist = int(step[1:])

            if dir == "U":
                dy = dist
            elif dir == "R":
                dx = dist
            elif dir == "D":
                dy = -dist
            elif dir == "L":
                dx = -dist

            nodes.append(Node(x + dx, y + dy))
        return nodes


def createWire(nodeList):
    """ Convert list of nodes to edges, then create and return edge list as Wire instance. """
    edges = []
    for i, toNode in enumerate(nodeList):
        if i == 0:
            continue

        fromNode = nodeList[i-1]
        edges.append(Edge(fromNode, toNode))

    return Wire(edges)


def partOne(ex=0):
    wireA, wireB = readInput(ex)
    intersections = wireA.findIntersections(wireB)
    minManhattan = min([n.manhattanToOrig() for n in intersections])
    return minManhattan

assert partOne(1) == 159
assert partOne(2) == 135
    
print(f"Part one: {partOne()}")


def partTwo(ex=0):
    wireA, wireB = readInput(ex)
    intersections = wireA.findIntersections(wireB)
    stepsA, stepsB = wireA.stepsToTargets(intersections), wireB.stepsToTargets(intersections)
    minSignalDelay = min([stepsA[i] + stepsB[i] for i in intersections])
    
    return minSignalDelay


assert partTwo(1) == 610
assert partTwo(2) == 410

print(f"Part two: {partTwo()}")