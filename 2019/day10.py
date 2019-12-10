import math
import os
import sys

filepath = os.path.join(sys.path[0], "day10.txt")

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
    ang = math.degrees(math.atan2(dx, dy))
    ang = (360 - ((ang + 180) % 360)) % 360  # Eww

    return ang


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

    print(pick, maxDetected)
    return hits


def partTwo():
    laser = (22, 19)
    # laser = (8, 3)
    asteroids.remove(laser)
    targets = []

    for ast in asteroids:
        dist = (laser[0] - ast[0])**2 + (laser[1] - ast[1])**2
        targets.append((ast, dist, findAngle(laser, ast)))
    targets.sort(key=lambda t: (t[2], t[1]))

    shots = 0
    while shots < 200 and len(targets):
        cycleShotDirections = set()
        shot = []

        for i in range(len(targets)):
            t = targets[i]
            target, dist, angle = t[0], t[1], t[2]

            if angle in cycleShotDirections:
                continue

            shots += 1
            # print("Shot " + str(shots) + " fired! Target destroyed: ",
            #       target, sep=" ")

            if shots == 200:
                winner = target
                print("partTwo output:", winner[0] * 100 + winner[1])
                break

            cycleShotDirections.add(angle)
            shot.append(t)

        for t in shot:
            targets.remove(t)


partOne()
partTwo()
