from itertools import islice

def read_input(filename: str = 'day3.txt'):
    with open(filename) as f:
        lines = (tuple(int(x) for x in line.split()) for line in f.readlines())

    return lines


def is_possible_triangle(x, y, z):
    top = max(x,y,z)
    return sum((x,y,z))-top > top


def part_one(lines):
    return sum(is_possible_triangle(*line) for line in lines)


def part_two(lines):

    possible = 0
    while True:
        rows = list(islice(lines, 3))
        if not rows:
            break

        for col in range(3):
            tri = tuple(rows[row][col] for row in range(3))
            possible += is_possible_triangle(*tri)

    return possible
    


if __name__ == '__main__':
    lines = read_input()
    # print(f'Part one: {part_one(lines)}')
    print(f'Part two: {part_two(lines)}')