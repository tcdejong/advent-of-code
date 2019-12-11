import math
import os
import sys

filepath = os.path.join(sys.path[0], "day10.txt")
# filepath = os.path.join(sys.path[0], "day10exp2.txt")

asteroids = []

with open(filepath) as file:
    y = 0
    for line in file:
        for x in range(len(list(line))):
            if line[x] == "#":
                asteroids.append((x, y))
        y += 1


def findAngle(a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    ang = math.degrees(math.atan2(dy, dx))
    if ang < 0:
        ang += 360

    ang += 90

    return ang % 360


def partOne():
    maxDetected = 0
    pick = (-1, -1)

    for ast in asteroids:
        hits = set()

        for target in asteroids:
            if ast == target:
                continue
            hits.add(findAngle(ast, target))

        count = len(hits)
        if count > maxDetected:
            pick, maxDetected = ast, count

    print(maxDetected, "detected from asteroid", pick, sep=" ")
    return pick


def partTwo():
    laser = partOne()
    asteroids.remove(laser)
    targets = []

    for ast in asteroids:
        dist = (laser[0] - ast[0])**2 + (laser[1] - ast[1])**2
        targets.append((ast, dist, findAngle(laser, ast)))
    targets.sort(key=lambda t: (t[2], t[1]))

    shots = 0
    lastDir = 361
    while targets:
        shot = []

        for t in targets:
            target, dist, angle = t
            if angle == lastDir:
                continue

            shots += 1
            lastDir = angle
            shot.append(t)

            if shots == 200:
                winner = target
                print("200th asteroid x*100+y:", winner[0] * 100 + winner[1])
                break

        for t in shot:
            targets.remove(t)


partTwo()
