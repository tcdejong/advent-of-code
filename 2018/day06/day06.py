import os
import sys


def loadInput():
    filePath = os.path.join(sys.path[0], "day6.txt")

    roots = []

    with open(filePath) as file:
        i = 0
        for line in file:
            line = line.strip()
            x, y = line.split(", ")
            roots.append(("r" + str(i), int(x), int(y)))
            i += 1

    return roots


def buildWorld(roots, worldOnly=False):
    # define world boundary to be a bounding box around all coordinates
    xmin, xmax = min(roots, key=lambda r: r[1])[1] - 1, max(roots, key=lambda r: r[1])[1] + 1
    ymin, ymax = min(roots, key=lambda r: r[2])[2] - 1, max(roots, key=lambda r: r[2])[2] + 1

    world = set([(x, y) for x in range(xmin, xmax) for y in range(ymin, ymax)])

    if worldOnly:
        return world
    else:
        return (world, xmin, xmax, ymin, ymax)


def partOne():
    roots = loadInput()
    world, xmin, xmax, ymin, ymax = buildWorld(roots)

    assignedTo = dict()
    infRoots = set()

    for p in world:
        closest = findClosestRoot(p, roots)

        if closest == -1:
            continue

        assert isinstance(p, tuple)

        x, y = p
        if not xmin <= x <= xmax or not ymin <= y <= ymax:
            infRoots.add(closest)
            continue

        if not closest in assignedTo:
            assignedTo[closest] = 0

        assignedTo[closest] += 1

    maxAssigned = 0
    for (r, _, _) in roots:
        if r in infRoots:
            continue

        if assignedTo[r] > maxAssigned:
            maxAssigned = assignedTo[r]

    print(maxAssigned)


def findClosestRoot(p, roots):
    x0, y0 = p

    distances = dict()

    for (r, x1, y1) in roots:
        d = abs(x1-x0) + abs(y1-y0)

        if d not in distances:
            distances[d] = set()

        distances[d].add(r)

    minDist = min(distances)
    if len(distances[minDist]) == 1:
        return distances[minDist].pop()
    else:
        return -1


def addedDistance(p, roots):
    x0, y0 = p
    res = 0

    for (_, x1, y1) in roots:
        res += abs(x1-x0) + abs(y1-y0)

    return res


def partTwo():
    roots = loadInput()
    world = buildWorld(roots, True)

    res = 0
    thresh = 10000
    for p in world:
        d = addedDistance(p, roots)
        if d < thresh:
            res += 1

    print(res)


partOne()
partTwo()
