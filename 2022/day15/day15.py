from typing import NamedTuple



class Point(NamedTuple):
    x: int
    y: int

SensorBeaconPair = tuple[Point, Point]


def read_input(filename: str = 'input.txt'):
    with open(filename) as f:
        data = tuple(parse_input_line(line) for line in f.readlines())

    return data


def parse_input_line(line:str) -> SensorBeaconPair:
    line = line.strip()
    sensor_raw, beacon_raw = line.split(": closest beacon is at x=")
    sensor_raw = sensor_raw.lstrip("Sensor at x=")
    sensor_raw = sensor_raw.split(", y=")
    sensor = Point(int(sensor_raw[0]), int(sensor_raw[1]))

    beacon_raw = beacon_raw.split(", y=")
    beacon = Point(int(beacon_raw[0]), int(beacon_raw[1]))
    
    return sensor, beacon


def manhattan_dist(p0: Point, p1: Point):
    return abs(p0.x - p1.x) + abs(p0.y - p1.y)


def all_coords_within_range(p: Point, maxdist: int) -> set[Point]:
    return set(
                    Point(p.x+dx, p.y+dy) 
                    for dx in range(-maxdist, maxdist + 1) 
                    for dy in range(-maxdist + abs(dx), maxdist - abs(dx) + 1)
                )


def all_coords_at_exact_dist(p: Point, dist: int) -> list[Point]:
    points = [Point(p.x+dx, p.y+(dist-abs(dx))) for dx in range(-dist, dist+1)]
    return points


def part_one(sensor_beacon_pairs: tuple[SensorBeaconPair, ...], y):
    sensor_beacon_distance_triplets = tuple((sensor, beacon, manhattan_dist(sensor, beacon)) for sensor, beacon in sensor_beacon_pairs)

    max_dist = max(sbd[2] for sbd in sensor_beacon_distance_triplets)
    min_x = min(beacon[0] for _, beacon in sensor_beacon_pairs) - max_dist
    max_x = max(beacon[0] for _, beacon in sensor_beacon_pairs) + max_dist

    no_beacon_possible = 0
    next_tile = False
    for x in range(min_x, max_x+1):
        tile = Point(x, y)
        for sensor, beacon, d_beacon in sensor_beacon_distance_triplets:
            d_tile = manhattan_dist(sensor, tile)

            if tile == beacon:
                next_tile = True
                break

            if d_tile <= d_beacon:
                next_tile = True
                no_beacon_possible += 1
                break

        if next_tile:
            next_tile = False
            continue

    return no_beacon_possible


def make_subranges(start, stop, n):
    d = stop-start
    div, remainder = divmod(d, n)
    subranges = [range(i*div, (i+1)*div) for i in range(n)]

    if remainder != 0:
        last = subranges[-1]
        subranges[-1] = range(last.start, stop)
        
    return subranges


def scan_area_bf(range_x, range_y, sensor_distances: tuple[tuple[Point, int]]):
    # Brute force, but skip tiles on a row where possible
    # Alternate strategies:
    # - scan outward from sensors starting at the distance to their nearest beacon +1

    scanned = 0
    jumped = 0

    py = range_y.start
    while py < range_y.stop:
        px = range_x.start
        while px < range_x.stop:
            tile = Point(px, py)
            scanned += 1

            distance_differences_to_beacon_per_sensor = [manhattan_dist(sensor, tile) - beacondist for sensor, beacondist in sensor_distances]

            if all(diff > 0 for diff in distance_differences_to_beacon_per_sensor):
                return tile
            
            jump_distance = abs(min(distance_differences_to_beacon_per_sensor))
            jumped += jump_distance
            px += max(jump_distance, 1)

            if scanned % 100_000 == 0:
                print(f'{scanned=} \t {jumped=}')
        
        py += 1



def scan_pulsing_out(sensor, dist, ):
    pass


# The brutest of forces!
def part_two_bf(sensor_beacon_pairs: tuple[SensorBeaconPair, ...], xy_limit):
    from concurrent.futures import ProcessPoolExecutor, as_completed

    workers = 6
    scan_ranges_x = make_subranges(0, xy_limit+1, workers)
    sensor_distances = tuple((sensor, manhattan_dist(sensor, beacon)) for sensor, beacon in sensor_beacon_pairs)
    
    with ProcessPoolExecutor(max_workers=workers) as executor:
        task_args = [(range_x, range(0,xy_limit+1), sensor_distances) for range_x in scan_ranges_x]
        futures = [executor.submit(scan_area_bf, *args) for args in task_args] # type: ignore
        
        for future in as_completed(futures):
            # retrieve the result
            result = future.result()

            if isinstance(result, Point):
                distress_beacon = result
                return distress_beacon.x * 4000000 + distress_beacon.y

    raise ValueError
    


if __name__ == '__main__':
    ex1 = read_input('ex1.txt')
    assert part_one(ex1, 10) == 26
    assert part_two_bf(ex1, 20) == 56000011

    print('==== Assertions Passed ====')

    sensor_beacon_pairs = read_input()
    # print(f'Part one: {part_one(sensor_beacon_pairs, 2000000)}')
    print(f'Part two: {part_two_bf(sensor_beacon_pairs, 4000000)}')