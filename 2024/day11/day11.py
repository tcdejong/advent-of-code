from functools import lru_cache
from collections import Counter


def read_input(filename: str = "input.txt"):
    with open(filename) as f:
        data = f.read().strip()

    stones = Counter([int(s) for s in data.split()])

    return stones

@lru_cache
def update_stone(stone: int):
    if stone == 0:
        return Counter([1])

    if len(str(stone)) % 2 == 0:
        stone_label = str(stone)
        num_chars = len(str(stone)) // 2
        left, right = int(stone_label[:num_chars]), int(stone_label[num_chars:])
        return Counter([left, right])

    return Counter([stone * 2024])


def blink(stones: Counter[int]):
    new_stones = Counter()
    for stone, occurrences in stones.items():
        single_expansion = update_stone(stone)
        total_expansion = Counter({k:v*occurrences for k,v in single_expansion.items()})

        if stone == 0:
            print(f'\t {stone=}, {single_expansion=}')

        new_stones += total_expansion
    return new_stones


def get_total_stones(stones: Counter[int]):
    return sum(stones.values())


def part_one(stones: Counter[int], num_blinks=25):
    print(f'initial:\n{stones}\n')
    for i in range(num_blinks):
        stones = blink(stones)
        print(i+1, '\t', stones)
    
    return get_total_stones(stones)


def part_two(stones: list[int]):
    raise NotImplementedError


if __name__ == "__main__":
    assert update_stone(1000) == Counter([10, 0])

    puzzle_input = read_input()
    example_input = read_input("ex1.txt")
    ex_2 = Counter([125, 17])

    assert part_one(ex_2, 6) == 22
    assert part_one(ex_2, 25) == 55312
    print(f"Part one: {part_one(puzzle_input)}")

    # assert part_two(example_input) == ...
    print(f'Part two: {part_one(puzzle_input, 75)}')
