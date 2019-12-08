import os
import sys

filePath = os.path.join(sys.path[0], "day6ex.txt")

roots = []

with open(filePath) as file:
    i = 0
    for line in file:
        line = line.strip()
        x, y = line.split(", ")
        roots.append(("r" + str(i), int(x), int(y)))
        i += 1


def getPointsAtDistance(root, d):
    r, rx, ry = root
    xmin, xmax, ymin, ymax = rx - d, rx + d, ry - d, ry + d

    top = [(r, x, ymax) for x in range(xmin, xmax)]
    right = [(r, xmax, y) for y in range(ymax, ymin, -1)]
    bot = [(r, x, ymin) for x in range(xmax, xmin, -1)]
    left = [(r, xmin, y) for y in range(ymin, ymax)]

    return top + right + bot + left


def classificationComplete():
    limit = (xmax + 1 - xmin) * (ymax + 1 - ymin)
    current = sum(list(map(len, classification.values())))

    return (current >= limit)


i = 0
classification = {
    "-": []
}

invalidRoots = set()
observed = set()
xvals, yvals = [x for (r, x, y) in roots], [y for (r, x, y) in roots]
xmin, xmax = min(xvals) - 1, max(xvals) + 1
ymin, ymax = min(yvals) - 1, max(yvals) + 1

for (r, x, y) in roots:
    classification[r] = []

while i < 350 and True:
    i += 1
    current = []
    counts = dict()

    for (r, x, y) in roots:
        neighbors = getPointsAtDistance((r, x, y), i)
        current += neighbors
        for (r, x, y) in neighbors:
            if not (x, y) in counts:
                counts[(x, y)] = 1
            else:
                counts[(x, y)] += 1

    for point in current:
        (r, x, y) = point
        if counts[(x, y)] == 1 and not (x, y) in observed:
            classification[r].append((x, y))
            if x < xmin or x > xmax or y < ymin or y > ymax:
                invalidRoots.add(r)
        observed.add((x, y))

    if classificationComplete() == True:
        break

for key in invalidRoots:
    classification.pop(key)
largest = max(classification, key=lambda k: len(classification[k]))
size = len(classification[largest])
print(largest, size)
