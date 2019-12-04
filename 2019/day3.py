# This is a pretty poor execution. It's sloppy.
# Next time I'd probably write a class for Nodes and Edges.
# Some refactoring wouldn't be bad either

import math
import os
import sys

H = "h"
V = "v"

inputPath = os.path.join(sys.path[0], "day3.txt")


def partOne(ex=0):
    stepsA, stepsB = parseInput(ex)

    nodesA = createNodes(stepsA)
    nodesB = createNodes(stepsB)

    nearestManhattanDistance = math.inf
    for i in range(0, len(nodesA) - 1):
        edgeA = (nodesA[i], nodesA[i+1])

        for j in range(0, len(nodesB) - 1):
            edgeB = (nodesB[j], nodesB[j+1])

            dist = intersectionDistance(edgeA, edgeB)

            if dist < nearestManhattanDistance:
                nearestManhattanDistance = dist

    return nearestManhattanDistance


def parseInput(ex=""):
    stepsA = []
    stepsB = []

    if ex == 1:
        stepsA = "R75,D30,R83,U83,L12,D49,R71,U7,L72".split(sep=",")
        stepsB = "U62,R66,U55,R34,D71,R55,D58,R83".split(sep=",")
    elif ex == 2:
        stepsA = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51".split(sep=",")
        stepsB = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7".split(sep=",")
    else:
        with open(inputPath) as rawData:
            stepsA = rawData.readline().strip().split(sep=",")
            stepsB = rawData.readline().strip().split(sep=",")

    return (stepsA, stepsB)


def createNodes(stepList):
    nodes = [(0, 0)]

    for step in stepList:
        current = nodes[-1]
        x, y = current[0], current[1]
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

        # each adjacent node in the list is connected, ergo nodes[z] and nodes[z+1] form an edge
        nodes.append((x + dx, y + dy))

    return nodes


def intersectionDistance(edgeA, edgeB, part2=False):
    Ax1, Ax2 = edgeA[0][0], edgeA[1][0]
    Ay1, Ay2 = edgeA[0][1], edgeA[1][1]
    Bx1, Bx2 = edgeB[0][0], edgeB[1][0]
    By1, By2 = edgeB[0][1], edgeB[1][1]

    orA, orB = H, H
    if Ax1 == Ax2:
        orA = V

    if Bx1 == Bx2:
        orB = V

    # assumes no touching corners: these are no wire *crossings*
    if orA == orB:
        return math.inf

    if orA == H:
        Hx1, Hx2, Hy = min(Ax1, Ax2), max(Ax1, Ax2), Ay1
        Vy1, Vy2, Vx = min(By1, By2), max(By1, By2), Bx1
    else:
        Hx1, Hx2, Hy = min(Bx1, Bx2), max(Bx1, Bx2), By1
        Vy1, Vy2, Vx = min(Ay1, Ay2), max(Ay1, Ay2), Ax1

    if Hx1 < Vx < Hx2 and Vy1 < Hy < Vy2:
        if part2:
            return (Vx, Hy)

        return abs(Vx) + abs(Hy)
    else:
        return math.inf


print(partOne())


def partTwo(ex=0):
    stepsA, stepsB = parseInput(ex)

    nodesA = createNodes(stepsA)
    nodesB = createNodes(stepsB)

    minSteps = math.inf
    for i in range(0, len(nodesA) - 1):
        edgeA = (nodesA[i], nodesA[i+1])

        for j in range(0, len(nodesB) - 1):
            edgeB = (nodesB[j], nodesB[j+1])

            res = intersectionDistance(edgeA, edgeB, True)
            if res != math.inf:
                steps = countSteps(res, stepsA) + countSteps(res, stepsB)
                if steps < minSteps:
                    minSteps = steps
    return minSteps


def edgeLength(edge):
    x1, y1, x2, y2 = edge[0][0], edge[0][1], edge[1][0], edge[1][1]
    if x1 == x2:
        return abs(abs(y2) - abs(y1))
    else:
        return abs(abs(x2) - abs(x1))


def countSteps(target, stepList):
    current = (0, 0)
    tx, ty = target[0], target[1]
    steps = 0

    for step in stepList:
        x, y = current[0], current[1]
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

        if dir == "U" or dir == "D":
            if x != tx:
                steps += dist
                current = (x, y+dy)
            else:
                steps += abs(ty - y)
                return steps
            pass
        else:
            if y != ty:
                steps += dist
                current = (x+dx, y)
            else:
                steps += abs(tx - x)
                return steps


print(partTwo())
