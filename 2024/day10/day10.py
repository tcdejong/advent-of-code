from collections import defaultdict
from dataclasses import dataclass

TPosition = tuple[int, int]


def read_input(filename: str = "input.txt"):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    map: dict[TPosition, int] = {(int(x), int(y)): int(height) for y, row in enumerate(data) for x, height in enumerate(row)}
    heights: defaultdict[int, set[TPosition]] = defaultdict(set)
    for y, row in enumerate(data):
        for x, height in enumerate(row):
            heights[int(height)].add((int(x), int(y)))

    return map, heights


@dataclass
class TrailMap:
    map: dict[TPosition, int]
    heights: defaultdict[int, set[TPosition]]

    def __post_init__(self):
        self.mapwidth = max(pos[0] for pos in self.map)
        self.mapheight = max(pos[1] for pos in self.map)

        # effectively doubly linked list
        self.successors: defaultdict[TPosition, set[TPosition]] = defaultdict(set)

        for pos in self.map:
            self.get_successors(pos)

    def get_neighbors(self, pos: TPosition):
        x0, y0 = pos
        neighbors: list[TPosition] = [(x0 + dx, y0 + dy) for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
        neighbors = [pos for pos in neighbors if 0 <= pos[0] <= self.mapwidth and 0 <= pos[1] <= self.mapheight]
        return neighbors

    def get_successors(self, pos: TPosition):
        height = self.map[pos]
        neighbors = {n for n in self.get_neighbors(pos) if self.map[n] == height + 1}
        self.successors[pos] = neighbors

    def find_all_trails(self, from_height=0):
        trail_starts = self.heights[from_height]
        trails = {pos: self.find_trails_from(pos) for pos in trail_starts}
        return trails

    def find_trails_from(self, pos: TPosition, route: list[TPosition] | None = None, seen: set[TPosition] | None = None):
        # Recursive DFS
        if route == None:
            route = []

        if seen == None:
            seen = set()

        route.append(pos)
        seen.add(pos)

        height = self.map[pos]
        if height == 9:
            return [route]

        successors = [pred for pred in self.successors[pos] if pred and pred not in seen]
        potential_routes = [self.find_trails_from(pred, [rcopy for rcopy in route], {s for s in seen}) for pred in successors]
        potential_routes = [route for routes in potential_routes for route in routes]

        return potential_routes


def part_one(puzzle_input):
    # sum of trailhead scores: # unique destinations from start
    map = TrailMap(*puzzle_input)
    trails = map.find_all_trails()
    trailhead_scores = {trailhead: len(set(route[-1] for route in routes)) for trailhead, routes in trails.items()}
    sum_of_scores = sum(score for score in trailhead_scores.values())
    return sum_of_scores


def part_two(puzzle_input):
    # sum of trailhead ratings: # unique routes to destinations
    map = TrailMap(*puzzle_input)
    trails = map.find_all_trails()
    sum_of_scores = sum(len(routes) for routes in trails.values())
    return sum_of_scores


if __name__ == "__main__":
    puzzle_input = read_input()
    example_input = read_input("ex1.txt")
    example_input2 = read_input("ex2.txt")

    trailmap = TrailMap(*example_input)

    assert part_one(example_input) == 1
    assert part_one(example_input2) == 36
    print(f"Part one: {part_one(puzzle_input)}")

    assert part_two(example_input2) == 81
    print(f"Part two: {part_two(puzzle_input)}")
