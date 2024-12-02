def read_input(filename: str = 'input.txt'):
    with open(filename) as f:
        lines = f.read().splitlines()
    
    calories = parse_input(lines)

    return calories


def parse_input(lines: list[str]) -> list[int]:
    return [int(line) if line != "" else 0 for line in lines]


def part_one(puzzle_input):
    current_max = 0
    current_sum = 0

    for line in puzzle_input:
        current_sum += line
        current_max = max(current_sum, current_max)

        if line == 0:
            current_sum = 0

    return current_max


def part_two(puzzle_input):
    top_three = [0, 0, 0]
    
    current_sum = 0

    for i, line in enumerate(puzzle_input):
        current_sum += line
        
        if line == 0 or i == len(puzzle_input)-1:
            top_three = sorted([*top_three, current_sum])[1:]
            current_sum = 0

    return sum(top_three)


if __name__ == '__main__':
    puzzle_input = read_input()

    ex1 = parse_input("""1000
    2000
    3000

    4000

    5000
    6000

    7000
    8000
    9000

    10000""".splitlines()) # type: ignore

    assert part_one(ex1) == 24000
    print(f'Part one: {part_one(puzzle_input)}')

    assert part_two(ex1) == 45000
    print(f'Part two: {part_two(puzzle_input)}')