SHAPE_SCORES = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

WINNING_MOVES = {
    'A': 'Y',
    'B': 'Z',
    'C': 'X',
}

def read_input(filename: str = '2022/day02.txt'):
    with open(filename) as f:
        data = [line.strip().split() for line in f.readlines()]

    return data

def round_score(their_move, my_move):
    score = SHAPE_SCORES[my_move]

    if WINNING_MOVES[their_move] == my_move:
        score += 6
    elif f'{their_move}{my_move}' in {'AX', 'BY', 'CZ'}:
        score += 3

    return score


def part_one(puzzle_input):
    return sum(round_score(their_move, my_move) for their_move, my_move in puzzle_input)


def part_two(puzzle_input):
    pass


if __name__ == '__main__':
    puzzle_input = read_input()
    ex1 = read_input('2022/day02ex1.txt')
    assert part_one(ex1) == 15

    print(f'Part one: {part_one(puzzle_input)}')
    # print(f'Part two: {part_two(puzzle_input)}')