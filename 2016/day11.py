from collections import namedtuple

Item = namedtuple('Item', 'element, type')
Elevator = namedtuple('Elevator', 'floor contents')

def read_input(filename: str = 'day11.txt'):
    with open(filename) as f:
        data = [line.strip().replace(',', '').replace('.', '').replace('-compatible', '').split() for line in f.readlines()]

    floors = [[] for _ in data]

    elements = {
        'generator': {}
        'microchip': {}
    }

    for floor, line in enumerate(data):
        for a, b in zip(line, line[1:]):
            if b == 'generator' or b == 'microchip':
                elements[b][a] = floor


    elevator = Elevator(0, [])

    return floors, elevator


def part_one(puzzle_input):
    pass


def part_two(puzzle_input):
    pass


if __name__ == '__main__':
    floors, elevator = read_input()

    # print(f'Part one: {part_one(puzzle_input)}')
    # print(f'Part two: {part_two(puzzle_input)}')
