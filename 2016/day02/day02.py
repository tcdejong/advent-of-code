ex1 = ["ULL",
"RRDDD",
"LURDL",
"UUUUD"]

KEYPAD = {(row,col): 3*row+col+1 for row in range(3) for col in range(3)}
SHITPAD = {
    (0, 2): '1',
    (1, 1): '2',
    (1, 2): '3',
    (1, 3): '4',
    (2, 0): '5',
    (2, 1): '6',
    (2, 2): '7',
    (2, 3): '8',
    (2, 4): '9',
    (3, 1): 'A',
    (3, 2): 'B',
    (3, 3): 'C',
    (4, 2): 'D'
}

def read_input(filename: str = 'input.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def find_button(clue, start_at=(1,1), keypad=KEYPAD):
    row, col = start_at
    for char in clue:
        _row, _col = row, col
        if char == 'U':
            row = row-1
        elif char == 'D':
            row = row+1
        elif char == 'L':
            col = col-1
        elif char == 'R':
            col = col+1
        
        if (row, col) not in keypad:
            row, col = _row, _col

    return (row, col)



def solve(keypad, instructions):
    button_pos = (1,1)
    button_vals = []
    for clue in instructions:
        button_pos = find_button(clue, button_pos, keypad)
        button_vals.append(keypad[button_pos])
    return "".join(str(x) for x in button_vals)


def part_one(instructions):
    print(solve(KEYPAD, instructions))


def part_two(instructions):
    print(solve(SHITPAD, instructions))


if __name__ == '__main__':
    instructions = read_input()
    part_one(instructions)
    part_two(instructions)


    