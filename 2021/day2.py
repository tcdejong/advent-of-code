from dataclasses import dataclass


def read_input():
    with open("day2.txt") as f:
        instructions = [(a, int(b)) for a, b in [x.split() for x in f.readlines()[:-1]]]

    return instructions



def part_one(instructions):
    @dataclass
    class Submarine:
        depth: int = 0
        h_pos: int = 0

        def perform_instruction(self, instruction: tuple[str, int]):
            op, dist = instruction

            if op == 'forward':
                self.h_pos += dist

            elif op == 'up':
                self.depth -= dist

            elif op == 'down':
                self.depth += dist
            
            else:
                raise NotImplementedError

    sub = Submarine()

    for inst in instructions:
        sub.perform_instruction(inst)

    return sub.h_pos * sub.depth



def part_two(instructions):
    @dataclass
    class Submarine:
        depth: int = 0
        h_pos: int = 0
        aim:   int = 0

        def perform_instruction(self, instruction: tuple[str, int]):
            op, dist = instruction

            if op == 'forward':
                self.h_pos += dist
                self.depth += self.aim * dist

            elif op == 'up':
                self.aim -= dist

            elif op == 'down':
                self.aim += dist
            
            else:
                raise NotImplementedError

    sub = Submarine()

    for inst in instructions:
        sub.perform_instruction(inst)

    return sub.h_pos * sub.depth





if __name__ == "__main__":
    instructions = read_input()
    
    print(f'Part one: {part_one(instructions)}')
    print(f'Part two: {part_two(instructions)}')