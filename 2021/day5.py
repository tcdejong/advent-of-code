import re
from collections import namedtuple, defaultdict

Line = namedtuple("Line", "x1 y1 x2 y2")

def read_input() -> list[Line]:
    mask = r"(\d+),(\d+) -> (\d+),(\d+)"
    with open("day5.txt") as f:
        raw = f.read()

    data = [Line(*map(int, groups)) for groups in re.findall(mask, raw)]
    return data
    
    

def part_one() -> int:
    lines = read_input()
    lines_hv = [l for l in lines if l.x1 == l.x2 or l.y1 == l.y2]
    grid = defaultdict(int)

    for l in lines_hv:
        x1, y1, x2, y2 = l

        xs = range(x1, x2+1) if x1 < x2 else range(x2, x1+1)
        ys = range(y1, y2+1) if y1 < y2 else range(y2, y1+1)
        points = [(x, y) for x in xs for y in ys]

        for xy in points: 
            grid[xy] += 1

    return (len([xy for xy in grid.values() if xy > 1]))


def part_two() -> int:
    lines = read_input()
    lines_d = [l for l in lines if l.x1 != l.x2 and l.y1 != l.y2]
    grid = defaultdict(int)

    for l in lines_d:
        x1, y1, x2, y2 = l

        xs = range(x1, x2+1) if x1 < x2 else range(x2, x1+1)
        ys = range(y1, y2+1) if y1 < y2 else range(y2, y1+1)
        points = [(x, y) for x in xs for y in ys]

        for xy in points: 
            grid[xy] += 1

    return (len([xy for xy in grid.values() if xy > 1]))


if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    # print(f'Part two: {part_two()}')
