from math import cos, sin, radians

NORTH = 0
EAST = 90
SOUTH = 180
WEST = 270

ex1 = [
    'F10',
    'N3',
    'F7',
    'R90',
    'F11',
]


class Ship:
    def __init__(self, instructions, part=1):
        self.facing = EAST
        self.pos_ns = 0
        self.pos_ew = 0
        self.instructions = instructions
        self.part = part

        if part == 2:
            self.wp_ns = 1
            self.wp_ew = 10


    def __repr__(self):
        return f'east {self.pos_ew}, north {self.pos_ns}, facing {self.facing}'


    def exec_instruction_p1(self, instruction):
        operation = instruction[0]
        param = int(instruction[1:])

        if operation == 'N':
            self.pos_ns += param
        elif operation == 'E':
            self.pos_ew += param
        elif operation == 'S':
            self.pos_ns -= param
        elif operation == 'W':
            self.pos_ew -= param

        elif operation == 'L':
            self.facing = (self.facing - param) % 360
        elif operation == 'R':
            self.facing = (self.facing + param) % 360

        elif operation == 'F':
            self.pos_ns += round(cos(radians(self.facing)) * param)
            self.pos_ew += round(sin(radians(self.facing)) * param)

        else:
            print(f'unknown instruction {instruction}')


    def exec_instruction_p2(self, instruction):
        operation = instruction[0]
        param = int(instruction[1:])

        if operation == 'N':
            self.wp_ns += param
        elif operation == 'E':
            self.wp_ew += param
        elif operation == 'S':
            self.wp_ns -= param
        elif operation == 'W':
            self.wp_ew -= param

        elif operation == 'L':
            rotation = 4 - (param // 90)
            [self.rotate_wp_cw() for _ in range(rotation)]
        
        elif operation == 'R':
            rotation = param // 90
            [self.rotate_wp_cw() for _ in range(rotation)]

        elif operation == 'F':
            self.pos_ns += self.wp_ns * param
            self.pos_ew += self.wp_ew * param

        else:
            print(f'unknown instruction {instruction}')


    def manhattan_pos(self):
        return abs(self.pos_ns) + abs(self.pos_ew)


    def rotate_wp_cw(self):
        self.wp_ew, self.wp_ns = self.wp_ns, -self.wp_ew


    def run(self):
        if self.part == 1:
            [self.exec_instruction_p1(i) for i in self.instructions]
        else:
            [self.exec_instruction_p2(i) for i in self.instructions]





def part_one(instructions):
    ship = Ship(instructions)
    ship.run()
    print(f'Part one: {ship.manhattan_pos()}')


def part_two(instructions):
    ship = Ship(instructions, part=2)
    ship.run()
    print(f'Part two: {ship.manhattan_pos()}')


def read_input():
    with open('day12.txt') as file:
        return file.readlines()


if __name__ == '__main__':
    instructions = read_input()
    part_one(instructions)
    part_two(instructions)