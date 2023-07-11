from string import ascii_lowercase, ascii_uppercase

def read_input(filename: str = '2022/day03.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    return data


def find_item_in_both_compartments(rucksack_contents):
    items_per_compartment = len(rucksack_contents) // 2
    items_comp1 = rucksack_contents[:items_per_compartment]
    items_comp2 = rucksack_contents[items_per_compartment:]
    assert len(items_comp1) == len(items_comp2)

    shared_item = set(list(items_comp1)) & set(list(items_comp2))
    assert len(shared_item) == 1

    return shared_item.pop()


def get_item_priority(item):
    ordered_aasci = ascii_lowercase + ascii_uppercase
    return 1 + ordered_aasci.find(item)


def part_one(puzzle_input):
    shared_items = [find_item_in_both_compartments(rucksack) for rucksack in puzzle_input]
    item_priorities = [get_item_priority(item) for item in shared_items]
    return sum(item_priorities)


def part_two(puzzle_input):
    sum_of_priorities = 0
    while len(puzzle_input) > 0:
        a, b, c = puzzle_input[:3]
        puzzle_input = puzzle_input[3:]

        item = set(list(a)) & set(list(b)) & set(list(c))
        assert len(item) == 1

        sum_of_priorities += get_item_priority(item.pop())
    
    return sum_of_priorities


if __name__ == '__main__':
    ex1 = read_input('2022/day03ex1.txt')
    assert part_one(ex1) == 157

    puzzle_input = read_input()
    print(f'Part one: {part_one(puzzle_input)}')

    assert part_two(ex1) == 70
    print(f'Part two: {part_two(puzzle_input)}')