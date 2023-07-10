import os
import sys

filepath = os.path.join(sys.path[0], "day1.txt")


def partOne():
    res = 0

    with open(filepath) as data:
        for line in data:
            val = int(line.strip())
            res += val

    return res


def partTwo():
    res = 0
    observed = [res]

    i = 0
    while True:
        with open(filepath) as data:
            for line in data:
                val = int(line.strip())
                res += val
                if res in observed:
                    return res
                else:
                    observed.append(res)

        # Output to show code still running
        if i % 10 == 0:
            print(i)

        i += 1


print("Part 1:", partOne(), sep=" ")
print("Part 2:", partTwo(), sep=" ")
