from collections import Counter, defaultdict


def read_input():
    with open("day6.txt") as f:
        data = f.read()

    data = list(map(int, data.split(",")))
    fish_counts = Counter(data)
    return fish_counts


def simulate_fish(ticks: int, fish = None):
    fish = fish if fish else read_input()
    for _ in range(ticks):
        fish = tick_fish(fish)
    return sum(fish.values())


def tick_fish(fish):
    new_fish = defaultdict(int)

    for timer in range(0,8):
        new_fish[timer] = fish[timer+1]

    new_fish[8] += fish[0]
    new_fish[6] += fish[0]

    return new_fish


def part_one():
    return simulate_fish(80)


def part_two():
    return simulate_fish(256)


if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')