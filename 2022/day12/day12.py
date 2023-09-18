from string import ascii_lowercase
from typing import NamedTuple


class Pos(NamedTuple):
    x: int
    y: int


START = 'S'
END = 'E'


def read_input(filename: str = 'input.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]
    
    heights = {c: i for i, c in enumerate(ascii_lowercase)}
    heights['S'] = heights['a']
    heights['E'] = heights['z']

    max_x = len(data[0])
    max_y = len(data)

    nodes = {(x,y): heights[data[y][x]] for x in range(max_x) for y in range(max_y)}

    startend: dict[str,Pos] = {}
    
    for y, line in enumerate(data):
        if START not in startend:
            x = line.find(START)
            if x >= 0:
                startend[START] = Pos(x, y)

        if END not in startend:
            x = line.find(END)
            if x >= 0:
                startend[END] = Pos(x, y)

        if START in startend and END in startend:
            break

    return nodes, startend[START], startend[END]


def valid_steps(heightmap, pos, seen, p2=False, max_x = None, max_y = None):
    positions = heightmap.keys()

    if not max_x:
        max_x = max(p[0] for p in positions)

    if not max_y:
        max_y = max(p[1] for p in positions)

    L = Pos(pos.x - 1, pos.y)
    R = Pos(pos.x + 1, pos.y)
    U = Pos(pos.x, pos.y - 1)
    D = Pos(pos.x, pos.y + 1)

    steps = [L, R, U, D]

    steps = [s for s in steps 
             if 
             s.x >= 0 and 
             s.y >= 0 and 
             s.x <= max_x and 
             s.y <= max_y and 
             s not in seen]

    if p2:
        steps = [s for s in steps if heightmap[s] >= heightmap[pos] -1]
    else:
        steps = [s for s in steps if heightmap[s] <= heightmap[pos] +1]


    return set(steps)



def part_one(heightmap, start_pos: Pos, end_pos: Pos):
    predecessors: dict[Pos, Pos] = {}
    prev_fill = set()
    prev_fill.add(start_pos)

    # Floodfill / BFS
    steps = 0
    while end_pos not in predecessors:
        steps += 1
        filled = set()
        for pos in prev_fill:
            new_adjacent = valid_steps(heightmap, pos, predecessors.keys())

            for step in new_adjacent:
                predecessors[step] = pos
                filled.add(step)
        
        prev_fill = filled    
    return steps


def part_two(heightmap, _, start_pos):
    predecessors: dict[Pos, Pos] = {}
    prev_fill = set()
    prev_fill.add(start_pos)

    # Floodfill / BFS
    steps = 0
    while True:
        steps += 1
        filled = set()
        for pos in prev_fill:
            new_adjacent = valid_steps(heightmap, pos, predecessors.keys(), p2=True)

            for step in new_adjacent:
                predecessors[step] = pos
                filled.add(step)
        
        prev_fill = filled

        if any(heightmap[p] == 0 for p in filled):
            break

    return steps

if __name__ == '__main__':
    inputs = read_input()
    ex_input = read_input('ex1.txt')
    assert part_one(*ex_input) == 31

    # print(f'Part one: {part_one(*inputs)}')

    assert part_two(*ex_input) == 29
    print(f'Part two: {part_two(*inputs)}')