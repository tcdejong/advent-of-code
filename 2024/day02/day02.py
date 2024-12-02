from itertools import pairwise


def read_input(filename: str = 'input.txt'):
    with open(filename) as f:
        data = [tuple(int(i) for i in line.strip().split()) for line in f.readlines()]

    return data


def is_safe(report: tuple[int, ...]):
    pairwise_report = zip(report, report[1:])
    deltas = [right-left for left, right in pairwise_report]

    result = all(1 <= d <= 3 for d in deltas) or all(1 <= -d <= 3 for d in deltas)

    if VERBOSE:
        print(f'{report=}, is_safe={result}')

    return result


def is_safe_tolerant(report: tuple[int, ...]):
    if VERBOSE:
        print(f'\nPt2 for {report}')

    if is_safe(report):
        return True
    
    deltas = [right-left for left, right in pairwise(report)]
    count_positive_deltas = sum(d > 0 for d in deltas)
    count_negative_deltas = sum(d < 0 for d in deltas)
    is_ascending = count_positive_deltas > count_negative_deltas

    if not is_ascending:
        report = tuple(reversed(report))

    for left_idx, (left, right) in enumerate(pairwise(report)):
        # if there is an issue at this index, either left of right causes problems.
        # try regular is_safe with either removed.
        
        delta = right-left

        if not 1 <= delta <= 3:
            dampened_report_options = [
                (*report[:left_idx], *report[left_idx+1:]),
                (*report[:left_idx+1], *report[left_idx+2:])
            ]

            if VERBOSE:
                print(f'testing by removing {left} or {right}')

            return any(is_safe(lst) for lst in dampened_report_options)

    raise RuntimeError("Unreachable code path detected!")


def part_one(puzzle_input):
    return sum(is_safe(report) for report in puzzle_input)


def part_two(puzzle_input: list[tuple[int, ...]]):
    return sum(is_safe_tolerant(report) for report in puzzle_input)


if __name__ == '__main__':
    VERBOSE = False
    puzzle_input_ex1 = read_input('ex1.txt')
    assert part_one(puzzle_input_ex1) == 2
    assert part_two(puzzle_input_ex1) == 4
    
    puzzle_input = read_input()
    print(f'Part one: {part_one(puzzle_input)}')
    print(f'Part two: {part_two(puzzle_input)}')

