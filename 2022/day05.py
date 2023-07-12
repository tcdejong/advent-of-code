from collections import namedtuple
Move = namedtuple('Move', 'times orig dest')

def read_input(filename: str = 'day05.txt'):
    with open(filename) as f:
        data = [line for line in f.read().splitlines()]

    for i, line in enumerate(data):
        if line == "":
            bottom_stack_row = i-1
            break

    
    row_content_indices = range(1, len(data[0]), 4)
    row_contents = [[row[c] for c in row_content_indices] for row in reversed(data[0:bottom_stack_row])]

    # transpose from rows to stacks
    stacks = list(zip(*row_contents))
    stacks = [[crate for crate in stack if crate != " "] for stack in stacks]
    
    moves = [parse_move(move) for move in data[bottom_stack_row+2:]]

    assert len(moves) > 0

    return stacks, moves


def parse_move(move_str):
    x = move_str.split()
    return Move(int(x[1]), int(x[3])-1, int(x[5])-1)


def part_one(puzzle_input):
    stacks, moves = puzzle_input

    for move in moves:
        for _ in range(move.times):
            crate = stacks[move.orig].pop()
            stacks[move.dest].append(crate)

    return "".join([stack[-1] for stack in stacks])


def part_two(puzzle_input):
    stacks, moves = puzzle_input

    for move in moves:
        crates = stacks[move.orig][-move.times:]
        stacks[move.orig] = stacks[move.orig][:-move.times]
        stacks[move.dest] = [*stacks[move.dest], *crates]

    return "".join([stack[-1] for stack in stacks])


if __name__ == '__main__':
    puzzle_input = read_input()
    p1 = part_one(puzzle_input)
    assert  p1 == "PSNRGBTFT"
    print(f'Part one: {p1}')


    ex1 = read_input('day05ex1.txt')
    assert part_two(ex1) == 'MCD'
    puzzle_input = read_input()
    print(f'Part two: {part_two(puzzle_input)}')