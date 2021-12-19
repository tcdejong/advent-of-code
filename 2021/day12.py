from collections import defaultdict, Counter

def read_input(filename: str = "day12.txt"):
    with open(filename) as f:
        edges = [line.strip().split('-') for line in f.readlines()]

    graph = defaultdict(set)

    for (O, D) in edges:
        graph[O].add(D)
        graph[D].add(O)

    return graph


def part_one():
    cave = read_input("day12.txt")
    path = ['start']
    paths = finish_path(path, cave)
    return len(paths)


def finish_path(path: list[str], cave: dict, part=1):
    pos = path[-1]

    if pos == "end":
        return [path]

    if part == 1:
        seen_small = set(x for x in path if x.islower())
        possible_steps = set(cave[pos]) - seen_small
    else:
        visit_counts = Counter(path)
        can_visit_twice = all(visit_counts[step] <= 1 or step.isupper() for step in path[1:])
        connected_caves = [p for p in cave[pos] if p != 'start']
        possible_steps = [step for step in connected_caves if step.isupper() or visit_counts[step] == 0 or (visit_counts[step] == 1 and can_visit_twice)]
        # possible_steps = cave[pos]

    if len(possible_steps) == 0:
        return

    finished_paths = [finish_path([*path, step], cave, part) for step in possible_steps]
    finished_paths = [p for p in finished_paths if p]
    finished_paths = [p for inner in finished_paths for p in inner]

    return finished_paths


def part_two():
    cave = read_input("day12.txt")
    path = ['start']
    paths = finish_path(path, cave, part=2)
    return len(paths)


if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')
