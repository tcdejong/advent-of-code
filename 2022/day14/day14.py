AIR = 0
STONE = 1
SAND = 2

SAND_ORIGIN = 500, 0


def read_input(filename: str = "input.txt"):
    with open(filename) as f:
        data = [tuple(tuple(int(v) for v in point.split(",")) for point in line.split(" -> ")) for line in f.readlines()]

    typed_data: list[tuple[tuple[int, int], ...]] = data

    return typed_data


def map_stone_locations(stone_paths: list[tuple[tuple[int, int], ...]]):
    map = {}
    for path in stone_paths:
        while len(path) >= 2:
            start = path[0]
            end = path[1]
            path = path[1:]

            points = get_coords_between_points(start, end)
            for point in points:
                map[point] = STONE

    return map


def get_coords_between_points(p0, p1):
    x0, y0 = p0
    x1, y1 = p1

    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0

    points = ((x, y) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1))

    return points


def produce_sand_unit(map, origin):
    # (x=0,y=0) is top left origin
    # right increments x
    # down increments y
    sand_pos = origin
    max_y = max(xy[1] for xy in map.keys())
    while True:
        x, y = sand_pos

        if y > max_y:
            return False

        tile_down = (x, y + 1)
        tile_down_left = (x - 1, y + 1)
        tile_down_right = (x + 1, y + 1)

        for tile in [tile_down, tile_down_left, tile_down_right]:
            if map.get(tile, AIR) == AIR:
                sand_pos = tile
                break
        else:
            map[sand_pos] = SAND
            return True


def print_map(map, spacing=2):
    min_x = min(xy[0] for xy in map.keys()) - spacing
    max_x = max(xy[0] for xy in map.keys()) + spacing
    min_y = min(xy[1] for xy in map.keys()) - spacing
    max_y = max(xy[1] for xy in map.keys()) + spacing

    SYM_AIR = "."
    SYM_STONE = "#"
    SYM_SAND = "O"

    SYMBOLS = {
        STONE: SYM_STONE,
        AIR: SYM_AIR,
        SAND: SYM_SAND,
    }

    grid = ["".join([SYMBOLS[map.get((x, y), AIR)] for x in range(min_x, max_x + 1)]) for y in range(min_y, max_y + 1)]

    print("\n".join(grid))


def part_one(puzzle_input):
    map = map_stone_locations(puzzle_input)

    sand_produced = 0
    while produce_sand_unit(map, SAND_ORIGIN):
        sand_produced += 1

    # print_map(map)
    return sand_produced


def part_two(puzzle_input):
    map = map_stone_locations(puzzle_input)

    floor_y = max(xy[1] for xy in map.keys()) + 2
    floor_x0 = SAND_ORIGIN[0] - floor_y - 5
    floor_x1 = SAND_ORIGIN[0] + floor_y + 5

    floor_l = (floor_x0, floor_y)
    floor_r = (floor_x1, floor_y)

    for tile in get_coords_between_points(floor_l, floor_r):
        map[tile] = STONE

    sand_produced = 0
    while produce_sand_unit(map, SAND_ORIGIN):
        sand_produced += 1
        if SAND_ORIGIN in map:
            break

    # print_map(map)
    return sand_produced


if __name__ == "__main__":
    puzzle_input = read_input()
    # puzzle_input = read_input('ex1.txt')
    map = map_stone_locations(puzzle_input)

    print(f"Part one: {part_one(puzzle_input)}")
    print(f"Part two: {part_two(puzzle_input)}")
