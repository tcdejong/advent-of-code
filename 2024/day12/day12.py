from dataclasses import dataclass

TPosition = tuple[int, int]
TEdge = set[TPosition]


@dataclass
class Region:
    plots: set[TPosition]

    def __post_init__(self):
        self.area = len(self.plots)
        self.perimiter = self.calc_perimiter()
        self.calc_sides()

    def calc_perimiter(self):
        return sum(4 - self.count_adjacent_plots_in_same_region(plot) for plot in self.plots)

    def count_adjacent_plots_in_same_region(self, pos: TPosition):
        return len(self.get_adjacent_plots_in_same_region(pos))

    def get_adjacent_plots_in_same_region(self, pos: TPosition):
        x0, y0 = pos
        adjacent = {(x0 + dx, y0 + dy) for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]} & self.plots
        return adjacent

    def get_adjacent_plots(self, pos: TPosition):
        x0, y0 = pos
        adjacent = {(x0 + dx, y0 + dy) for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]}
        return adjacent

    def calc_sides(self):
        perimeter_plots = {plot for plot in self.plots if self.get_adjacent_plots(plot) != self.get_adjacent_plots_in_same_region(plot)}

        left_perimeter_plots = {(x, y) for (x, y) in perimeter_plots if (x - 1, y) not in self.plots}
        right_perimeter_plots = {(x, y) for (x, y) in perimeter_plots if (x + 1, y) not in self.plots}
        top_perimeter_plots = {(x, y) for (x, y) in perimeter_plots if (x, y - 1) not in self.plots}
        bot_perimeter_plots = {(x, y) for (x, y) in perimeter_plots if (x, y + 1) not in self.plots}

        left_edges = self.detect_edges_1_orientation(left_perimeter_plots, (0, 1))
        right_edges = self.detect_edges_1_orientation(right_perimeter_plots, (0, 1))
        top_edges = self.detect_edges_1_orientation(top_perimeter_plots, (1, 0))
        bot_edges = self.detect_edges_1_orientation(bot_perimeter_plots, (1, 0))

        edges = [edge for edge in [*left_edges, *right_edges, *top_edges, *bot_edges]]

        self.num_edges = len(edges)

        return edges

    def detect_edges_1_orientation(self, candidate_plots: set[TPosition], dxdy: tuple[int, int]):
        edges: list[TEdge] = []
        new_edge: TEdge = set()
        dx, dy = dxdy

        while candidate_plots:
            edge_start = candidate_plots.pop()
            new_edge.add(edge_start)
            x0, y0 = edge_start

            x, y = x0, y0
            while (x + dx, y + dy) in candidate_plots:
                x = x + dx
                y = y + dy
                new_edge.add((x, y))

            x, y = x0, y0
            while (x - dx, y - dy) in candidate_plots:
                x = x - dx
                y = y - dy
                new_edge.add((x, y))

            edges.append(new_edge)
            candidate_plots = candidate_plots - new_edge
            new_edge = set()

        return edges

    def calc_price(self):
        return self.area * self.perimiter

    def calc_price_discounted(self):
        return self.area * self.num_edges

    def __repr__(self) -> str:
        return f"Region({self.area=}, {self.perimiter=})"


def read_input(filename: str = "input.txt"):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    return data


def find_regions(map: list[str]):
    # floodfill for regions
    seen: set[TPosition] = set()

    regions: list[Region] = []
    for y, row in enumerate(map):
        for x, _ in enumerate(row):
            if (x, y) not in seen:
                new_region = floodfill_region_from_pos((x, y), map)
                regions.append(new_region)
                seen = seen | new_region.plots

    return regions


def part_one(puzzle_input: list[str]):
    regions = find_regions(puzzle_input)
    return sum(r.calc_price() for r in regions)


def part_two(puzzle_input: list[str]):
    regions = find_regions(puzzle_input)
    return sum(r.calc_price_discounted() for r in regions)


def floodfill_region_from_pos(pos: TPosition, map: list[str]):
    x, y = pos
    char = map[y][x]

    maxx = len(map[0])
    maxy = len(map)

    to_explore: set[TPosition] = {pos}
    seen: set[TPosition] = set()
    tiles: set[TPosition] = {pos}

    while to_explore:
        tile = to_explore.pop()
        x0, y0 = tile

        seen.add(tile)
        if map[y0][x0] != char:
            continue

        tiles.add(tile)

        neighbors = {(x0 + dx, y0 + dy) for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)] if 0 <= x0 + dx < maxx and 0 <= y0 + dy < maxy}
        neighbors = neighbors - seen

        to_explore = to_explore | neighbors

    return Region(tiles)


if __name__ == "__main__":
    puzzle_input = read_input()
    example_input1 = read_input("ex1.txt")
    example_input2 = read_input("ex2.txt")
    example_input3 = read_input("ex3.txt")

    regions = find_regions(example_input1)

    assert part_one(example_input1) == 140
    assert part_one(example_input2) == 772
    assert part_one(example_input3) == 1930
    print(f"Part one: {part_one(puzzle_input)}")

    assert part_two(example_input1) == 80
    assert part_two(example_input2) == 436
    print(f'Part two: {part_two(puzzle_input)}')
