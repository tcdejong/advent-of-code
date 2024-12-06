TPosition = tuple[int, int]
TDirection = tuple[int, int]
TGuard = tuple[TPosition, TDirection]

DIR_U: TDirection = (0, -1)
DIR_R: TDirection = (1, 0)
DIR_D: TDirection = (0, 1)
DIR_L: TDirection = (-1, 0)

SYMBOL_GUARD_U = "^"
SYMBOL_GUARD_R = ">"
SYMBOL_GUARD_D = "v"
SYMBOL_GUARD_L = "<"

GUARD_SYMBOLS: dict[TDirection, str] = {
    DIR_U: SYMBOL_GUARD_U,
    DIR_R: SYMBOL_GUARD_R,
    DIR_D: SYMBOL_GUARD_D,
    DIR_L: SYMBOL_GUARD_L,
}

SYMBOL_OBSTRUCTION = "#"
SYMBOL_EMPTY = "."
SYMBOL_VISITED = "X"


def read_input(filename: str = "input.txt"):
    with open(filename) as f:
        data = f.readlines()

    return data


class PatrolMap:
    def __init__(self, data: list[str]):
        self.obstuctions: set[TPosition] = set()
        self.guard_pos: TPosition
        self.guard_dir: TDirection

        self.dimensions = (len(data[0]), len(data))
        self.parse_map(data)

        self.guard_visited: set[TGuard] = set()

    def parse_map(self, data: list[str]):
        self.obstuctions = {(x, y) for y, row in enumerate(data) for x, char in enumerate(row) if char == SYMBOL_OBSTRUCTION}
        for y, row in enumerate(data):
            for x, char in enumerate(row):
                if char == SYMBOL_GUARD_U:
                    self.guard_pos = (x, y)
                    self.guard_dir = DIR_U

    def simulate_guard(self):
        while not self.guard_left_area():
            if self.guard_is_looping():
                return True

            self.guard_visited.add((self.guard_pos, self.guard_dir))
            next_space: TPosition = tuple(sum(xy) for xy in zip(self.guard_pos, self.guard_dir))

            if next_space in self.obstuctions:
                self.rotate_guard()
            else:
                self.guard_pos = next_space

        return False

    def guard_left_area(self):
        x, y = self.guard_pos
        return x < 0 or x >= self.dimensions[0] or y < 0 or y >= self.dimensions[1]  # >= because dimensionsare based on len

    def rotate_guard(self):
        next_dir = {DIR_U: DIR_R, DIR_R: DIR_D, DIR_D: DIR_L, DIR_L: DIR_U}

        self.guard_dir = next_dir[self.guard_dir]

    def guard_is_looping(self):
        return (self.guard_pos, self.guard_dir) in self.guard_visited

    def print_map(self):
        map = [list("." * self.dimensions[0]) for _ in range(self.dimensions[1])]

        for x, y in self.obstuctions:
            map[y][x] = SYMBOL_OBSTRUCTION

        for (x, y), _ in self.guard_visited:
            try:
                map[y][x] = SYMBOL_VISITED
            except IndexError:
                pass

        try:
            x, y = self.guard_pos
            map[y][x] = GUARD_SYMBOLS[self.guard_dir]
        except IndexError:
            pass

        map = "\n".join("".join(line) for line in map)
        print(map)


def part_one(puzzle_input):
    game = PatrolMap(puzzle_input)
    game.simulate_guard()
    visited = {pos for (pos, _) in game.guard_visited}

    return len(visited)


def part_two(puzzle_input):
    maxx = len(puzzle_input[0])
    maxy = len(puzzle_input)

    options: set[TPosition] = set()

    for x in range(maxx):
        print(f'{x=}/{maxx}')
        for y in range(maxy):
            game = PatrolMap(puzzle_input)
            
            if (x,y) == game.guard_pos:
                continue
            
            game.obstuctions.add((x,y))
            if game.simulate_guard():
                options.add((x,y))
    
    print(options)
    return len(options)



if __name__ == "__main__":
    puzzle_input = read_input()
    example_input = read_input("ex1.txt")

    assert part_one(example_input) == 41
    print(f"Part one: {part_one(puzzle_input)}")

    assert part_two(example_input) == 6
    print(f'Part two: {part_two(puzzle_input)}')
