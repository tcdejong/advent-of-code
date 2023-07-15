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


def tail_too_far(head, tail):
    res = abs(head[0] - tail[0]) > 1 or abs(head[1] - tail[1]) > 1
    # print(head, tail, res)
    return res


def add_elemwise(a, b):
    assert len(a) == len(b)
    return tuple(sum(x) for x in zip(a,b))


def part_one(puzzle_input):
    head = (0,0)
    tail = (0,0)

    visited_by_tail = set()

    for direction, steps in puzzle_input:
        v = DIRECTIONS[direction]
        for _ in range(steps):
            _head = head
            head = add_elemwise(head, v)

            if tail_too_far(head, tail):
                tail = _head

            print(head, tail)
            assert not tail_too_far(head, tail)

            visited_by_tail.add(tail)

    return len(visited_by_tail)


def part_two(puzzle_input):
    pass


if __name__ == '__main__':
    puzzle_input = read_input()
    print(f'Part one: {part_one(puzzle_input)}')
    # print(f'Part two: {part_two(puzzle_input)}')