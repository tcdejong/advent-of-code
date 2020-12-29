from collections import defaultdict

def read_input(fp='day17.txt'):
    cubes = defaultdict(bool)
    with open(fp) as file:
        for row, line in enumerate(file.readlines()):
            for col, c in enumerate(line):
                cubes[row, col, 0] = True if c == "#" else False

    return cubes


def count_active_neighbors(old_cubes: dict) -> dict:
    active_neighbors = defaultdict(int)

    for (x,y,z), active in old_cubes.items():
        if active == False:
            continue

        for x_ in range(x-1, x+2):
            for y_ in range(y-1,y+2):
                for z_ in range(z-1, z+2):
                    if x_ == y_ == z_ == 0:
                        continue
                    active_neighbors[x_,y_,z_] += 1

    return active_neighbors


def cycle(old_cubes):    
    # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.

    active_neighbors = count_active_neighbors(old_cubes)
    coordinates = set([*old_cubes.keys(), *active_neighbors.keys()])
    new_cubes = defaultdict(bool)

    for xyz in coordinates:
        if old_cubes[xyz]:
            if active_neighbors[xyz] in {2,3}:
                new_cubes[xyz] = True

        elif active_neighbors[xyz] == 3:
            new_cubes[xyz] = True

    return new_cubes


def count_active_cubes(cubes):
    return sum(val for val in cubes.values())


if __name__ == '__main__':
    cubes = read_input('day17ex.txt')

    for i in range(6):
        cubes = cycle(cubes)

    print(count_active_cubes(cubes))