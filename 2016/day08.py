from collections import Counter


def read_input(filename: str = 'day8.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]
    return data

class Screen:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._screen = generate_new_screen(width, height)

    def get_row(self, row_num):
        return [x for x in self._screen[row_num]]

    def set_row(self, row_num, row_vals):
        assert len(row_vals) == self._width
        self._screen[row_num] = row_vals

    def get_col(self, col_num):
        return [self._screen[row_num][col_num] for row_num in range(self._height)]

    def set_col(self, col_num, col_vals):
        assert len(col_vals) == self._height
        for row_num in range(self._height):
            self._screen[row_num][col_num] = col_vals[row_num]

    def exec_instruction(self, instr: str):
        if instr.startswith("rect"):
            width, height = [int(x) for x in instr.lstrip("rect ").split("x")]
            return self.rect(width, height)

        if instr.startswith("rotate row y="):
            row, n = [int(x) for x in instr.lstrip("rotate row y=").split(" by ")]
            return self.rotate_row(row, n)

        if instr.startswith("rotate column x="):
            col, n = [int(x) for x in instr.lstrip("rotate column x=").split(" by ")]
            return self.rotate_col(col, n)

        print(instr)
        raise NotImplementedError
    

    def rect(self, width, height):
        for row_num in range(height):
            line = [ON for _ in range(width)]
            self._screen[row_num][0:width] = line


    def rotate_row(self, row, n):
        vals = self.get_row(row)
        n = n % self._width
        shifted_vals = vals[-n:] + vals[:-n]
        self.set_row(row, shifted_vals)


    def rotate_col(self, col, n):
        vals = self.get_col(col)
        n = n % self._height
        shifted_vals = vals[-n:] + vals[:-n]
        self.set_col(col, shifted_vals)


    def __str__(self):
        rows = ["".join(row) for row in self._screen]
        return "\n".join(rows)


def generate_new_screen(width: int, height: int):
    return [
        [OFF for _ in range(width)] for __ in range(height)
    ]


def part_one(puzzle_input):
    screen = Screen(*SCREEN_DIM)
    for instr in puzzle_input:
        screen.exec_instruction(instr)

    counts = Counter()
    for row in screen._screen:
        counts.update(row)

    print(screen)

    return counts[ON]



if __name__ == '__main__':
    SCREEN_DIM = (50, 6)
    ON = "#"
    OFF = "."
    puzzle_input = read_input()

    print(f'Part one: {part_one(puzzle_input)}')
    # print(f'Part two: {part_two(puzzle_input)}')