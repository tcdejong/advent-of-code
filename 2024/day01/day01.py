from collections import Counter

def read_input(filename: str = 'input.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    data = [[int(num) for num in line.split()] for line in data]
    data = [[pair[0] for pair in data], [pair[1] for pair in data]]

    return data


def part_one(puzzle_input):
    left_lst, right_lst = puzzle_input
    left_lst = sorted(left_lst)
    right_lst = sorted(right_lst)

    pairs = zip(left_lst, right_lst, strict=True)

    total_distance = sum(abs(left-right) for left, right in pairs)

    return total_distance



def part_two(puzzle_input):
    left_lst, right_lst = puzzle_input
    
    right_counts = Counter(right_lst)

    similarity_score = sum(left * right_counts[left] for left in left_lst)

    return similarity_score


if __name__ == '__main__':
    puzzle_input_ex1 = read_input('ex1.txt')
    assert part_one(puzzle_input_ex1) == 11

    puzzle_input = read_input()
    print(f'Part one: {part_one(puzzle_input)}')

    assert part_two(puzzle_input_ex1) == 31
    print(f'Part two: {part_two(puzzle_input)}')