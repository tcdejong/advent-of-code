import os
import sys

inputPath = os.path.join(sys.path[0], "day3.txt")


def parseInput(filePath):
    steps = []
    with open(inputPath) as rawData:
        steps = rawData.read().split(sep=",")

    print(steps)
