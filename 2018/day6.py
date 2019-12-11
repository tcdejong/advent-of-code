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


# def getPointsAtDistance(root, d):
#     rx, ry = root
#     xmin, xmax, ymin, ymax = rx - d, rx + d, ry - d, ry + d

#     top = [(x, ymax) for x in range(xmin, xmax)]
#     right = [(xmax, y) for y in range(ymax, ymin, -1)]
#     bot = [(x, ymin) for x in range(xmax, xmin, -1)]
#     left = [(xmin, y) for y in range(ymin, ymax)]

#     res = set()
#     res.update(top, right, bot, left)

#     return res

def getNeighbors(workingSet, world):
    res = dict()
    for r in workingSet:
        res[r] = set()
        for (x, y) in workingSet[r]:
            res[r].update([(x-1, y), (x+1, y), (x, y-1), (x, y+1)])

    return res


def buildWorld(roots):
    # define world boundary to be a bounding box around all coordinates
    xmin, xmax = min(roots, key=lambda r: r[1])[
        1] - 1, max(roots, key=lambda r: r[1])[1] + 1
    ymin, ymax = min(roots, key=lambda r: r[2])[
        2] - 1, max(roots, key=lambda r: r[2])[2] + 1

    world = set([(x, y) for x in range(xmin, xmax)
                 for y in range(ymin, ymax)])

    return world


def partOne():
    roots = loadInput()
    world = buildWorld(roots)

    assignedTo = dict()
    workingNodes = dict()
    observed = set()

    for (r, x, y) in roots:
        observed.add((x, y))
        assignedTo[r] = set([(x, y)])
        workingNodes[r] = set([(x, y)])

    while True:
        neighbors = getNeighbors(workingNodes, world)
        counts = dict()

        for r, x, y in roots:
            for p in neighbors[r]:
                if p in observed:
                    continue

                if not p in counts:
                    counts[p] = 1
                else:
                    counts[p] += 1

        for r in neighbors:
            workingNodes[r] = set()
            for p in neighbors[r]:
                if not p in counts:
                    continue

                if counts[p] == 1:
                    assignedTo[r].add(p)
                    workingNodes[r].add(p)

            observed.update(neighbors[r])

        if observed.issuperset(world):
            break
        else:
            workingNodes = neighbors

    largest = 0
    for r in assignedTo:
        if assignedTo[r] <= world and len(assignedTo[r]) > largest:
            largest = len(assignedTo[r])

    print(largest)


def addedDistance(p, roots):
    x0, y0 = p
    res = 0

    for (r, x1, y1) in roots:
        res += abs(x1-x0) + abs(y1-y0)

    return res


def partTwo():
    roots = loadInput()
    world = buildWorld(roots)

    res = 0
    thresh = 10000
    for p in world:
        d = addedDistance(p, roots)
        if d < thresh:
            res += 1

    print(res)


partOne()  # Slow, refactor TODO
# partTwo()
