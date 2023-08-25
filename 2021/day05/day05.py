import re
from collections import namedtuple, defaultdict

Line = namedtuple("Line", "x1 y1 x2 y2")

def read_input() -> list[Line]:
    mask = r"(\d+),(\d+) -> (\d+),(\d+)"
    with open("day5.txt") as f:
        raw = f.read()

    data = [Line(*map(int, groups)) for groups in re.findall(mask, raw)]
    return data


def generate_points(l: Line) -> list[tuple[int, int]]:
    x1, y1, x2, y2 = l

    if x1 == x2 or y1 == y2:
        xs = range(x1, x2+1) if x1 < x2 else range(x2, x1+1)
        ys = range(y1, y2+1) if y1 < y2 else range(y2, y1+1)
        return [(x, y) for x in xs for y in ys]
    else:
        dx = 1 if x1 <= x2 else -1
        dy = 1 if y1 <= y2 else -1
        points = list(zip(range(x1, x2+dx, dx), range(y1, y2+dy, dy)))
        return points


def calc_overlap(part: int) -> int:
    lines = read_input()
    if part == 1:
        lines = [l for l in lines if l.x1 == l.x2 or l.y1 == l.y2]
    grid = defaultdict(int)

    for l in lines:
        points = generate_points(l)
        for xy in points: 
            grid[xy] += 1

    return (len([xy for xy in grid.values() if xy > 1]))


def part_one():
    return calc_overlap(1)

def part_two():
    return calc_overlap(2)


if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')

