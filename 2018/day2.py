import copy
import os
import sys
from functools import reduce

inputPath = os.path.join(sys.path[0], "day2.txt")
outputPath = os.path.join(sys.path[0], "day2-output.txt")


def partOne():
    exactlyTwice = []
    exactlyThrice = []

    with open(inputPath) as data:
        for line in data:
            # prepare processing of line
            chars = {}
            text = line.strip()

            # count character occurences
            for char in text:
                if char in chars:
                    chars[char] += 1
                else:
                    chars[char] = 1

            if 3 in chars.values():
                exactlyThrice.append(text)

            if 2 in chars.values():
                exactlyTwice.append(text)

    # Generate and print checksum
    print("Checksum:", len(exactlyTwice) * len(exactlyThrice), sep=" ")

    # Write output for part two
    output = exactlyTwice.copy()
    output.extend(exactlyThrice)
    return output


def partTwo():
    candidates = partOne()

    for index in range(len(candidates)):
        id = candidates[index]
        for target in candidates[index+1:]:
            comparisons = zip(id, target, range(len(id)))
            differences = []
            for el in comparisons:
                if el[0] != el[1]:
                    differences.append(el[2])
                if len(differences) > 1:
                    break
            if len(differences) > 1:
                continue
            elif len(differences) == 1:
                boundary = differences[0]
                print(boundary)

                res = id[:boundary] + id[boundary+1:]
                return res


print("Part two:", partTwo(), sep=" ")
