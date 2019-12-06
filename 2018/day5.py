import os
import sys

filePath = os.path.join(sys.path[0], "day5.txt")

with open(filePath) as file:
    challengeInput = file.read().strip()


def partOne(polymer):
    madeChanges = True
    while madeChanges:
        madeChanges = False
        i = 0
        while i < len(polymer) - 1:
            this = polymer[i]
            that = polymer[i + 1]

            if this.casefold() == that.casefold():
                if (this.islower() and that.isupper()) or (this.isupper() and that.islower()):
                    polymer = polymer[:i] + polymer[i+2:]
                    madeChanges = True
                    i -= 1
            i += 1

    print("Remaining polymer length: " + str(len(polymer)))
    return len(polymer)


def partTwo(polymer):
    units = set(list(polymer.lower()))

    shortestLen = len(polymer)

    for unit in units:
        unit = str(unit)
        newPoly = str(polymer).replace(unit, "").replace(unit.upper(), "")

        newLen = partOne(newPoly)

        if newLen < shortestLen:
            shortestLen = newLen

    print("Shortest polymer length: " + str(newLen))


# partOne(challengeInput)
partTwo(challengeInput)
