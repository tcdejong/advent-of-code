from collections import namedtuple

Heading = namedtuple('Heading', 'vx vy')
Position = namedtuple('Position', 'x y')

NORTH = Heading(0, 1)
EAST = Heading(1, 0)
SOUTH = Heading(0, -1)
WEST = Heading(-1, 0)

def read_input(filename: str="day1.txt") -> list[str]:
    """Read the input and return a list of strings, each string being 1 step."""
    with open(filename) as f:
        contents = f.read().strip()
        instructions = contents.split(", ")
    
    return instructions


def rotate(heading: Heading, dir: str) -> Heading:
    """Given a heading and a turning direction, return the new heading."""
    if dir == 'L':
        if heading == NORTH:
            return WEST
        if heading == WEST:
            return SOUTH
        if heading == SOUTH:
            return EAST
        if heading == EAST:
            return NORTH

        raise ValueError

    if dir == 'R':
        if heading == NORTH:
            return EAST
        if heading == EAST:
            return SOUTH
        if heading == SOUTH:
            return WEST
        if heading == WEST:
            return NORTH

        raise ValueError
    raise ValueError


def part_one(steps, part_two=False):
    heading = NORTH
    pos = Position(0, 0)
    visited = set(pos)

    for step in steps:
        dir, dist = step[0], int(step[1:])
        heading = rotate(heading, dir)

        if part_two:
            for _ in range(dist):
                pos = Position(pos.x + heading.vx, pos.y + heading.vy)
                if pos in visited:
                    print(f'Final position: {pos}')
                    return abs(pos.x) + abs(pos.y)
                visited.add(pos)
        else:
            pos = Position(pos.x + dist * heading.vx, pos.y + dist * heading.vy)

    print(f'Final position: {pos}')
    return abs(pos.x) + abs(pos.y)


def part_two(steps):
    return part_one(steps, True)


if __name__ == '__main__':    
    puzzle_input = read_input()

    assert part_one(puzzle_input) == 230
    assert part_two(steps=["R8", "R4", "R4", "R8"]) == 4

    print(f'Part two: {part_two(puzzle_input)}')