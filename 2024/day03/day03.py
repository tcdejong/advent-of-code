import re

def read_input(filename: str = 'input.txt'):
    with open(filename) as f:
        data = f.read().strip()

    return data


def part_one(puzzle_input):
    pattern = r'mul\(\d+,\d+\)'
    instructions = re.findall(pattern, puzzle_input)
    print(instructions)
    values = sum(do_mul(instruction) for instruction in instructions)
    return values


def do_mul(mul_str:str):
    left, right = mul_str.split(',')
    left = int(left.lstrip('mul('))
    right = int(right.rstrip(')'))
    return left * right


def part_two(puzzle_input):
    pattern = r"(mul\(\d+,\d+\))|(do\(\))|(don't\(\))"
    instructions: list[str] = re.findall(pattern, puzzle_input)
    instructions = [x for instr in instructions for x in instr if x]

    mul_enabled = True
    res = 0
    for instr in instructions:
        if instr == "don't()":
            mul_enabled = False
        elif instr == 'do()':
            mul_enabled = True
        elif mul_enabled:
            res += do_mul(instr)

    return res


if __name__ == '__main__':
    example_input = read_input('ex1.txt')
    example_input2 = read_input('ex2.txt')

    assert part_one(example_input) == 161
    assert part_two(example_input2) == 48
    
    puzzle_input = read_input()
    print(f'Part one: {part_one(puzzle_input)}')
    print(f'Part two: {part_two(puzzle_input)}')