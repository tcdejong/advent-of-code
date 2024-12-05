from collections import defaultdict


def read_input(filename: str = "input.txt"):
    with open(filename) as f:
        data = f.read().strip()
        raw_order_rules, updates = data.split("\n\n")

    order_rules: list[tuple[int, int]] = [
        tuple(int(x) for x in line.split("|")) for line in raw_order_rules.splitlines()
    ]
    updates = [tuple(int(x) for x in line.split(",")) for line in updates.splitlines()]

    rule_dict: defaultdict[int, set[int]] = defaultdict(set)

    for rule in order_rules:
        page, predecessor = rule
        rule_dict[page].add(predecessor)

    return rule_dict, updates


def is_valid_update(rule_dict: defaultdict[int, set[int]], update):
    seen: set[int] = set()
    for page in update:
        predecessors = rule_dict[page]

        seen_predecessors = seen.intersection(predecessors)
        if seen_predecessors:
            return False

        seen.add(page)

    return True


def fix_update(
    rule_dict: defaultdict[int, set[int]], update: tuple[int, ...]
) -> tuple[int, ...]:
    seen: set[int] = set()
    fixed: list[int] = []
    for page in update:
        seen.add(page)
        predecessors = rule_dict[page]

        seen_predecessors = seen.intersection(predecessors)
        if seen_predecessors:
            first_seen_idx = min(fixed.index(pred) for pred in seen_predecessors)
            fixed.insert(first_seen_idx, page)
        else:
            fixed.append(page)

    return tuple(fixed)


def part_one(rule_dict: defaultdict[int, set[int]], updates: list[tuple[int, ...]]):
    valid_updates = [update for update in updates if is_valid_update(rule_dict, update)]
    middle_indexes = [(len(update) + 1) // 2 - 1 for update in valid_updates]
    sum_of_middle_numbers = sum(
        update[idx] for update, idx in zip(valid_updates, middle_indexes)
    )
    return sum_of_middle_numbers


def part_two(rule_dict: defaultdict[int, set[int]], updates: list[tuple[int, ...]]):
    fixed_updates = [fix_update(rule_dict, update) for update in updates if not is_valid_update(rule_dict, update)]
    middle_indexes = [(len(update) + 1) // 2 - 1 for update in fixed_updates]
    sum_of_middle_numbers = sum(
        update[idx] for update, idx in zip(fixed_updates, middle_indexes)
    )
    return sum_of_middle_numbers


if __name__ == "__main__":
    puzzle_input = read_input()
    example_input = read_input("ex1.txt")

    assert part_one(*example_input) == 143
    print(f"Part one: {part_one(*puzzle_input)}")

    assert part_two(*example_input) == 123
    print(f"Part two: {part_two(*puzzle_input)}")
