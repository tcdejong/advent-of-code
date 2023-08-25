example = [
    1721,
    979,
    366,
    299,
    675,
    1456,
]


def part_one(expenses, target = 2020):
    seen = set()

    for a in expenses:
        remainder = target - a
        if remainder in seen:
            return a * remainder
        else:
            seen.add(a)


def part_two(expenses):
    target = 2020

    for a in expenses:
        remainder = target - a
        res = part_one(expenses, remainder)

        if res:
            return a * res

    
def main():
    with open("day1.txt") as file:
        expenses = [int(line) for line in file.read().split()]

    print("Part one:", part_one(expenses))
    print("Part two:", part_two(expenses))


if __name__ == '__main__':
    main()