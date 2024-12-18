from collections import defaultdict
from itertools import combinations

TPosition = tuple[int,int]
TMap = defaultdict[str, set[TPosition]]

def read_input(filename: str = 'input.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    bounds = (len(data[0]), len(data))

    antennas: TMap = defaultdict(set)
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char in ".#":
                continue

            antennas[char].add((x,y))


    return antennas, bounds


def calc_antinodes(antenna_positions: set[TPosition]):
    # Imagine a = (0,0) and b = (2,3)
    # dxdy = (-2,-3)
    # antinode = ax + dxdy
    # antinode = bx - dxdy
    
    antinodes: set[TPosition] = set()

    pairs = combinations(antenna_positions, 2)
    for (ax, ay), (bx, by) in pairs:
        dx = ax - bx
        dy = ay - by

        antinodes.add((ax + dx, ay + dy))
        antinodes.add((bx - dx, by - dy ))
    
    return antinodes


def calc_antinodes2(antenna_positions: set[TPosition], bounds: tuple[int,int]):   
    antinodes: set[TPosition] = set()

    pairs = combinations(antenna_positions, 2)
    for (ax, ay), (bx, by) in pairs:
        dx = ax - bx
        dy = ay - by

        x, y = ax, ay
        while True:
            antinodes.add((x,y))
            x,y = x+dx, y+dy
            if not(0 <= x < bounds[0] and 0 <= y < bounds[1]):
                break

        x, y = ax, ay
        while True:
            antinodes.add((x,y))
            x,y = x-dx, y-dy
            if not(0 <= x < bounds[0] and 0 <= y < bounds[1]):
                break
    
    return antinodes


def part_one(antennas: TMap, bounds: tuple[int,int]):
    antinodes = {antinode for _, antenna_positions in antennas.items() for antinode in calc_antinodes(antenna_positions)}
    antinodes = {pos for pos in antinodes if 0 <= pos[0] < bounds[0] and 0 <= pos[1] < bounds[1]}
    return(len(antinodes))


def part_two(antennas: TMap, bounds: tuple[int,int], verbose=False):
    antinodes = {antinode for _, antenna_positions in antennas.items() for antinode in calc_antinodes2(antenna_positions, bounds)}
    antinodes = {node for node in antinodes if node != set()} # clear empty sets
    return(len(antinodes))


if __name__ == '__main__':
    puzzle_input = read_input()
    example_input = read_input('ex1.txt')
    example_input3 = read_input('ex3.txt')

    assert part_one(*example_input) == 14
    print(f'Part one: {part_one(*puzzle_input)}')

    assert part_two(*example_input) == 34
    assert part_two(*example_input3, verbose=True) == 9
    print(f'Part two: {part_two(*puzzle_input)}')