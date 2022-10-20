def read_input(filename: str = 'day2.txt'):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


def find_button(clue, start_at=5):
    row, col = 1, 1
    for char in clue:
        if char == 'U':
            row = max(0, row-1)
        elif char == 'D':
            row = min(2, row+1)
        elif char == 'L':
            col = max(0, col-1)
        elif char == 'R':
            col = min(2, row+1)


if __name__ == '__main__':
    KEYPAD = {(row,col): 3*row+col+1 for row in range(3) for col in range(3)}

    instructions = read_input()
    code = [find_button(clue) for clue in instructions]

    print(code)