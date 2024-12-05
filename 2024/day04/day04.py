def read_input(filename: str = "input.txt"):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    return data


TPosition = tuple[int, int]
TPosWithDir = tuple[int, int, int]


class WordSearch:
    def __init__(self, lines: list[str]):
        self.lines = lines
        self.num_rows = len(lines)
        self.num_cols = len(lines[0])

    def get_char_positions(
        self, x: int, y: int, dir: int, num_chars: int
    ) -> list[TPosition]:
        # dir is an int of 0-7 where 0 is up, 2 right, 4 down, 6 left, and the odds are the diagonals
        # steps holds tuples of (dx, dy) for each direction

        assert 0 <= dir <= 7
        dxdys = {
            0: (0, -1),
            1: (1, -1),
            2: (1, 0),
            3: (1, 1),
            4: (0, 1),
            5: (-1, 1),
            6: (-1, 0),
            7: (-1, -1),
        }

        dx, dy = dxdys[dir]

        if not 0 <= x < self.num_cols:
            return []
        if not 0 <= y < self.num_rows:
            return []
        if not 0 <= x + dx * (num_chars - 1) < self.num_cols:
            return []
        if not 0 <= y + dy * (num_chars - 1) < self.num_rows:
            return []

        char_positions = [(x + dx * i, y + dy * i) for i in range(num_chars)]
        # print(f'{x=}, {y=},{dx=}, {dy=}, {dir=},\n{char_positions=}')
        return char_positions

    def get_chars(self, x: int, y: int, dir: int, num_chars: int) -> str:
        positions = self.get_char_positions(x, y, dir, num_chars)
        return "".join(self.lines[y][x] for (x, y) in positions)

    def check_for_word(self, x: int, y: int, word: str) -> list[TPosWithDir]:
        char = self.lines[y][x]
        if not word.startswith(char):
            return []

        results = [
            (x, y, d) for d in range(8) if word == self.get_chars(x, y, d, len(word))
        ]
        return results

    def find_word_occurrences(self, word: str):
        positions = [
            pos
            for x in range(self.num_cols)
            for y in range(self.num_rows)
            for pos in self.check_for_word(x, y, word)
        ]

        return positions

    # def show_occurrence(self, occurrence: TPosWithDir, num_chars: int):
    #     occurrence_chars = self.get_char_positions(*occurrence, num_chars)
    #     self.show_chars(occurrence_chars)

    def show_all_occurrences(self, word: str):
        occurrences = self.find_word_occurrences(word)
        occurrence_chars = [
            pos
            for occurrence in occurrences
            for pos in self.get_char_positions(*occurrence, len(word))
        ]
        self.show_chars(occurrence_chars)

    def show_chars(self, chars: list[TPosition]):
        grid = [["." for x in range(self.num_cols)] for y in range(self.num_rows)]

        for x, y in chars:
            grid[y][x : x + 1] = self.lines[y][x]

        grid = ["".join(grid[y]) for y in range(self.num_rows)]
        grid = "\n".join(grid)
        print(grid)


def part_one(puzzle_input: list[str]):
    ws = WordSearch(puzzle_input)
    occurrences = ws.find_word_occurrences("XMAS")
    # print(occurrences)
    # print(len(occurrences))
    return len(occurrences)


def part_two(puzzle_input: list[str]):
    ws = WordSearch(puzzle_input)
    occurrences = ws.find_word_occurrences("MAS")

    # only consider diagonals, make it a set
    occurrences = [(x, y, d) for (x, y, d) in occurrences if d in {1, 3, 5, 7}]
    occurrences = set(occurrences)
    found: set[tuple[TPosWithDir, TPosWithDir]] = set()

    for occ in occurrences:
        x, y, d = occ

        candidates: dict[int, set[TPosWithDir]] = {
            1: {
                (x, y - 2, 3),
                (x + 2, y, 7),
            },
            3: {
                (x, y + 2, 1),
                (x + 2, y, 5),
            },
            5: {
                (x - 2, y, 3),
                (x, y + 2, 7),
            },
            7: {
                (x - 2, y, 1),
                (x, y - 2, 5),
            },
        }

        valid = occurrences.intersection(candidates[d])
        assert len(valid) <= 1

        if valid:
            hit = valid.pop()
            if (hit, occ) not in found:
                found.add((occ, hit))

    return len(found)


if __name__ == "__main__":
    puzzle_input = read_input()
    example_input = read_input("ex1.txt")

    ws = WordSearch(example_input)

    assert part_one(example_input) == 18
    print(f"Part one: {part_one(puzzle_input)}")

    assert part_two(example_input) == 9
    print(f"Part two: {part_two(puzzle_input)}")
