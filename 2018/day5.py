import os
import sys

filePath = os.path.join(sys.path[0], "day5.txt")

with open(filePath) as file:
    challengeInput = file.read().strip()


def partOne(polymer, output=True):
    i = 0
    while i < len(polymer) - 1:
        this = polymer[i]
        that = polymer[i + 1]

        if this.casefold() == that.casefold():
            if (this.islower() and that.isupper()) or (this.isupper() and that.islower()):
                polymer = polymer[:i] + polymer[i+2:]
                i = max(0, i - 2)
        i += 1

    if output:
        print("Remaining polymer length: " + str(len(polymer)))
    return len(polymer)


def partTwo(polymer):
    units = set(list(polymer.lower()))
    shortestLen = len(polymer)

    for unit in units:
        unit = str(unit)
        newPoly = str(polymer).replace(unit, "").replace(unit.upper(), "")
        newLen = partOne(newPoly, False)
        if newLen < shortestLen:
            shortestLen = newLen

    print("Shortest polymer length: " + str(shortestLen))


partOne(challengeInput)
partTwo(challengeInput)
