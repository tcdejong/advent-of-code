from itertools import pairwise

def read_input(filename: str = 'day09.txt'):
    with open(filename) as f:
        data = [line.split() for line in f.readlines()]
        data = [tuple([line[0], int(line[1])]) for line in data] 

    return data

DIRECTIONS = {
    'R': (1, 0),
    'L': (-1, 0),
    'U': (0, 1),
    'D': (0, -1)
}


class Knot:
    def __init__(self, x, y):
        self.x: int = x
        self.y: int = y
        self._x = x
        self._y = y

    def move(self, v: tuple[int,int]):
        self._x = self.x
        self._y = self.y
        
        self.x += v[0]
        self.y += v[1]

    def is_pulled_by(self, knot: 'Knot'):
        return abs(self.x - knot.x) > 1 or abs(self.y - knot.y) > 1
    
    def pull_direction(self, knot: 'Knot'):
        v = [0,0]

        if self.x != knot.x:
            v[0] = -1 if self.x > knot.x else 1
        if self.y != knot.y:
            v[1] = -1 if self.y > knot.y else 1

        return (v[0], v[1])

    def be_pulled_by(self, knot: 'Knot'):
        if not self.is_pulled_by(knot):
            return
        
        v = self.pull_direction(knot)

        self.move(v)
        

def part_two(puzzle_input, rope_length = 10, print_steps = False):
    rope = [Knot(0,0) for _ in range(rope_length)]
    head = rope[0]
    tail = rope[-1]
    visited_by_tail = set()

    for direction, steps in puzzle_input:
        for _ in range(steps):
            v = DIRECTIONS[direction]
            head.move(v)

            for h, t in pairwise(rope):
                t.be_pulled_by(h)
            
            tail_pos = (tail.x, tail.y)
            visited_by_tail.add(tail_pos)

            if print_steps:
                print_rope(rope)

    return(len(visited_by_tail))


def print_rope(rope: list[Knot]):
    s = Knot(0,0)

    if not all(isinstance(x, Knot) for x in rope):
        print(rope)

    min_x = min(rope, key=lambda p: p.x)
    max_x = min(rope, key=lambda p: p.x)
    min_y = min(rope, key=lambda p: p.y)
    max_y = min(rope, key=lambda p: p.y)

    min_x = min(min_x.x, -1)
    max_x = max(max_x.x + 1, 5)
    min_y = min(min_y.y, -1)
    max_y = max(max_y.y + 1, 5)

    SYMBOL_EMPTY = "."
    SYMBOL_HEAD = "H"
    SYMBOL_START = "S"

    grid = {(x,y): SYMBOL_EMPTY for x in range(min_x, max_x) for y in range(min_y, max_y)}
    grid[0, 0] = SYMBOL_START

    for i, elem in enumerate(rope):
        x,y = elem.x, elem.y
        grid[x, y] = str(i) if i > 0 else SYMBOL_HEAD

    
    for y in range(max_y-1, min_y, -1):
        line = "".join([grid[x,y] for x in range(min_x, max_x)])
        print(line)

    print()


if __name__ == '__main__':
    puzzle_input = read_input()
    print(f'Part one: {part_two(puzzle_input, rope_length=2)}')
    print(f'Part two: {part_two(puzzle_input)}')