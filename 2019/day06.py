import os
import sys

filepath = os.path.join(sys.path[0], "day6.txt")

orbits = dict()
orbitsInverse = dict()

with open(filepath) as file:
    for line in file:
        line = line.strip()
        if line != "":
            inner, outer = line.split(")")

            if not inner in orbits:
                orbits[inner] = []

            orbits[inner].append(outer)
            orbitsInverse[outer] = inner


def getOrbits(obj, depth):
    depth += 1
    if not obj in orbits:
        return 0

    direct, indirect = depth * len(orbits[obj]), 0
    for val in orbits[obj]:
        indirect += getOrbits(val, depth)

    return direct + indirect


def partOne():

    total = getOrbits("COM", 0)
    print(total)


def partTwo():
    pathYouCom = findPathToCOM("YOU")
    pathSanCom = findPathToCOM("SAN")

    merger = ""

    for orbit in pathYouCom:
        if orbit in pathSanCom:
            merger = orbit
            break

    i = pathYouCom.index(merger)
    j = pathSanCom.index(merger)

    segmA = pathYouCom[1:i+1]
    segmB = pathSanCom[:j]
    segmB.reverse()

    jumps = len(segmA) + len(segmB)
    print(jumps)


def findPathToCOM(obj):
    path = [orbitsInverse[obj]]

    while path[-1] != "COM":
        nextOrbit = orbitsInverse[path[-1]]
        path.append(nextOrbit)

    return path


# partOne()
partTwo()
