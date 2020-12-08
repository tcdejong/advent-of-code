# One instruction per line
# Each instruction consists of an operation
# - acc, jmp, nop
# And an argument
# A single number like +4 or -20

# acc increeases or decreases a global variable 'accumulator' by the value in the argument
# jmp jumps to a new instruction relative to itself. E.g. jmp +2 skips the next instruction
# nop stands for no operation

from collections import defaultdict


class HandheldGameConsole:
    def __init__(self, instructions, accumulator=0):
        self.instructions = instructions
        self.accumulator = 0
        self.pointer = 0

        self.ops = {
            'acc': self.acc,
            'jmp': self.jmp,
            'nop': self.nop,
        }


    def acc(self, arg):
        self.accumulator += arg
        self.pointer += 1


    def jmp(self, arg):
        self.pointer += arg


    def nop(self, arg):
        self.pointer += 1


    def run(self):
        visited = defaultdict(int)

        while True:
            if self.pointer in visited:
                print(f'Infinite loop! {self.accumulator=}')
                return False

            if self.pointer >= len(self.instructions):
                print(f'Program finished! {self.accumulator=}')
                return True

            visited[self.pointer] += 1

            op, arg = self.instructions[self.pointer]
            self.ops[op](arg)


    @classmethod
    def from_raw_input(cls, raw_input="day8.txt"):
        with open(raw_input) as file:
            instructions = [(op, int(arg)) for op, arg in (line.strip().split() for line in file.readlines())]

        return cls(instructions)


def part_one():
    console = HandheldGameConsole.from_raw_input()
    console.run()


def part_two():
    _console = HandheldGameConsole.from_raw_input()

    for i, (op, arg) in enumerate(_console.instructions):
        if op == 'acc':
            continue
        
        console = HandheldGameConsole.from_raw_input()

        if op == 'nop':
            console.instructions[i] = ('jmp', arg)
            if console.run():
                return
        elif op == 'jmp':
            console.instructions[i] = ('nop', arg)
            if console.run():
                return

if __name__ == '__main__':
    part_two()