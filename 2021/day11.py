def read_input(filename: str = "day11.txt"):
    with open(filename) as f:
        data = [list(line.strip()) for line in f.readlines() if line.strip() != ""]
    
    data = [list(map(int,line)) for line in data]
    octopi = {(x, y): data[y][x] for x in range(10) for y in range(10)}
    return octopi


def part_one():
    octopi = read_input("day11.txt")
    flashes = 0

    for _ in range(100):
        octopi, step_flashes = step_once(octopi)
        flashes += step_flashes

    return flashes



def step_once(octopi):
    has_flashed = set()

    # increase energy by 1
    for pos, energy in octopi.items():
        octopi[pos] = energy + 1

    # for each at energy 10, flash
    for pos in octopi:
        octopi, has_flashed = flash(pos, octopi, has_flashed)

    # for flashing octopi, set energy to 0
    for pos in has_flashed:
        octopi[pos] = 0

    return octopi, len(has_flashed)


def flash(pos, octopi: dict, has_flashed: set):
    energy = octopi[pos]
    if energy > 9 and pos not in has_flashed:
        has_flashed.add(pos)
        nbs = get_neighbors(pos) - has_flashed

        for nb in nbs:
            octopi[nb] += 1
            octopi, has_flashed = flash(nb, octopi, has_flashed)

    return octopi, has_flashed


def get_neighbors(pos: tuple[int,int]):
    """get chebyshev neighbors to input position, respecting grid boundaries."""
    x0, y0 = pos
    minx = max(0, x0-1)
    maxx = min(9, x0+1) + 1
    miny = max(0, y0-1)
    maxy = min(9, y0+1) + 1

    nbs = [(x,y) for x in range(minx,maxx) for y in range(miny, maxy) if x != x0 or y != y0]
    return set(nbs)


def print_octopi(octopi):
    for y in range(10):
        print(" ".join(str(octopi[(x,y)]) for x in range(10)))


def part_two():
    octopi = read_input("day11.txt")

    step = 0
    while True:
        octopi, step_flashes = step_once(octopi)
        step += 1

        if step_flashes == 100:
            return step


if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')