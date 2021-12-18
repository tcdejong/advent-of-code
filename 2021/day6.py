from collections import Counter


def read_input() -> list[int]:
    with open("day6.txt") as f:
        data = f.read()

    return list(map(int, data.split(",")))

def simulate_fish(ticks: int):
    fish = read_input()

    for i in range(ticks):
        # print(i, len(fish))
        fish = tick_fish(fish)

    return len(fish)

def tick_fish(fish) -> list[int]:
    fish = [f-1 for f in fish] # tick
    new_fish = [8 for f in fish if f < 0] # spawn
    fish = [6 if f < 0 else f for f in fish] # correct
    return fish + new_fish # return

def part_one():
    return simulate_fish(80)

def part_two():
    return simulate_fish(256)



if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')