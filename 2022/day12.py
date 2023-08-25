from string import ascii_lowercase
from typing import NamedTuple


class Pos(NamedTuple):
    y: int
    x: int


START = 'S'
END = 'E'




def read_input(filename: str = 'day12.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]
    
    heights = {c: i for i, c in enumerate(ascii_lowercase)}
    heights['S'] = heights['a']
    heights['E'] = heights['z']

    max_x = len(data[0])
    max_y = len(data)

    nodes = {(x,y): data[y][x] for x in range(max_x) for y in range(max_y)}

    startend: dict[str,Pos] = {}
    
    for y, line in enumerate(data):
        if START not in startend:
            x = line.find(START)
            if x >= 0:
                startend[START] = (x, y)
        if END not in startend:
            x = line.find(START)
            if x >= 0:
                startend[END] = (x, y)

        if START in startend and END in startend:
            break

    return nodes, startend[START], startend[END]


def valid_steps(heightmap, pos, seen):
    max_x = len(heightmap[0])
    max_y = len(heightmap)

    L = Pos(pos.x - 1, pos.y)
    R = Pos(pos.x + 1, pos.y)
    U = Pos(pos.x, pos.y - 1)
    D = Pos(pos.x, pos.y + 1)

    steps = [L, R, U, D]
    steps = [s for s in steps if s.x >= 0 and s.y >= 0 and s.x < max_x and s.y < max_y and s not in seen]

    return set(steps)



def part_one(heightmap, start_pos, end_pos):
    seen = set()
    open = set(start_pos)

    while True:
        if end_pos in seen:
            break
        if len(open) == 0:
            break






def part_two(heightmap):
    pass


if __name__ == '__main__':
    inputs = read_input()
    print(f'Part one: {part_one(*inputs)}')
    # print(f'Part two: {part_two(heightmap)}')