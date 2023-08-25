from collections import defaultdict

def read_input(fp='day17.txt', part=1):
    """
    Read puzzle input and convert it to a dictionary
    Use 3D or 4D coordinates depending on optional arg 'part'
    Coordinates are dictionary keys, boolean values represent if a cube is active
    """

    cubes = defaultdict(bool)
    with open(fp) as file:
        for row, line in enumerate(file.readlines()):
            for col, c in enumerate(line):
                if c == "#":
                    key = (row, col, 0) if part == 1 else (row, col, 0, 0)
                    cubes[key] = True

    return cubes


def count_active_neighbors(cubes: dict) -> dict:
    """ 
    Return a dictionary where the key is a coordinate
    and the value is the number of active neighbors.

    For each active cube, add 1 to the value of the neighboring coordinates
    """ 
    active_neighbors = defaultdict(int)

    for pos, active in cubes.items():
        if active == False:
            continue

        # Read coordinates depending on 3D or 4D labels
        x, y, z = pos if len(pos) == 3 else pos[:3]
        w = pos[-1]

        # Increment active neighbor counters
        # Skip self, we increment *neighbors*. 
        # At least 1 dimension must differ
        for x_ in range(x-1, x+2):
            for y_ in range(y-1,y+2):
                for z_ in range(z-1, z+2):
                    if len(pos) == 3:
                        if x_ != x or y_ != y or z_ != z:
                            active_neighbors[x_,y_,z_] += 1
                    else:
                        for w_ in range(w-1, w+2):
                            if x_ != x or y_ != y or z_ != z or w_ != w:
                                active_neighbors[x_,y_,z_,w_] += 1

    return active_neighbors


def cycle(old_cubes: dict) -> dict:
    """ 
    Take a dictionary with board state
    Apply the activation/deactivation rules once
    Return a dictionary with the new game state
    """

    # Game rules
    # If a cube is active and exactly 2 or 3 of its neighbors are also active, the cube remains active. Otherwise, the cube becomes inactive.
    # If a cube is inactive but exactly 3 of its neighbors are active, the cube becomes active. Otherwise, the cube remains inactive.

    active_neighbors = count_active_neighbors(old_cubes)
    coordinates = set([*old_cubes.keys(), *active_neighbors.keys()])
    new_cubes = defaultdict(bool)

    for xyz in coordinates:
        if old_cubes[xyz] and active_neighbors[xyz] in {2,3}:
                new_cubes[xyz] = True
        elif not old_cubes[xyz] and active_neighbors[xyz] == 3:
            new_cubes[xyz] = True

    return new_cubes


def count_active_cubes(cubes: dict) -> int:
    return sum(cubes.values())


def print_cubes(cubes: dict) -> None:
    coords = [key for key in cubes.keys() if cubes[key]]    

    if coords and len(coords[0]) != 3:
        print('print_cubes not compatible with part 2!')
        return
    
    min_x = min(x for x, y, z in coords)
    min_y = min(y for x, y, z in coords)
    min_z = min(z for x, y, z in coords)
    max_x = max(x for x, y, z in coords)
    max_y = max(y for x, y, z in coords)
    max_z = max(z for x, y, z in coords)

    for z in range(min_z, max_z + 1):
        print(f'{z=}:\n')

        lines = [['#' if cubes[x,y,z] else '.' for x in range(min_x, max_x + 1)] for y in range(min_y, max_y + 1)]
        lines = [''.join(line) for line in lines]
        lines = '\n'.join(str(line) for line in lines)

        print(lines, '\n\n')



if __name__ == '__main__':
    cubes = read_input('day17.txt', part=2)

    for i in range(6):
        print(f'Start of cycle {i=}: \t {count_active_cubes(cubes)} active cubes')
        cubes = cycle(cubes)
    
    print('###########################################')
    print('Final active cubes:\t', count_active_cubes(cubes))