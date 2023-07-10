def calcFuel(moduleMasses, part=1):
    fuel = 0
    for el in moduleMasses:
        latest = calcModuleFuel(el)
        fuel += latest

        while latest > 0 and part == 2:
            latest = calcModuleFuel(latest)
            fuel += latest

    return fuel


def calcModuleFuel(mass):
    return max(mass // 3 - 2, 0)


# Read input
with open("day1.txt") as file:
    moduleMasses = [int(x) for line in file if len(x := line.strip()) > 0]

# Part one provided test cases
assert calcModuleFuel(12) == 2
assert calcModuleFuel(14) == 2
assert calcModuleFuel(1969) == 654
assert calcModuleFuel(100756) == 33583

print("Part 1:", calcFuel(moduleMasses))


# Part two provided test cases
assert calcFuel([14], 2) == 2
assert calcFuel([1969], 2) == 966
assert calcFuel([100756], 2) == 50346

print("Part 2:", calcFuel(moduleMasses, 2))