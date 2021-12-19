import heapq

def read_input(filename: str = "day9.txt"):
    with open(filename) as f:
        return f.read().splitlines(False)


def part_one():
    heightmap = read_input()
    lowpoints = find_lowpoints(heightmap)
    risk = sum(int(heightmap[y][x])+1 for x,y in lowpoints)
    return risk


def find_lowpoints(heightmap):
    x_mins = [find_row_mins(row) for row in heightmap]
    y_max = len(heightmap) - 1

    lowpoints = []
    for y, xs in enumerate(x_mins):
        for x in xs:
            if y != 0 and heightmap[y-1][x] <= heightmap[y][x]:
                continue

            if y != y_max and heightmap[y+1][x] <= heightmap[y][x]:
                continue

            lowpoints.append((x,y))
    return lowpoints



def find_row_mins(row: str):
    """Find the local minimums in this row, only considering neighbors in the same row"""
    row = [int(c) for c in row]
    max_i = len(row) - 1

    lows = []

    for i, z in enumerate(row):
        if i == 0 and row[i+1] > z:
            lows.append(i)
        elif i == max_i and row[i-1] > z:
            lows.append(i)
        elif row[i-1] > z and z < row[i+1]:
            lows.append(i)

    return lows


def part_two():
    heightmap = read_input("day9.txt")
    lowpoints = find_lowpoints(heightmap)
    basins = [determine_basin(lp, heightmap) for lp in lowpoints]
    a,b,c = heapq.nlargest(3, basins)
    return a*b*c
    

def determine_basin(lowpoint: tuple[int, int], heightmap):
    seen = set()
    size = 0
    queue = {lowpoint}

    while len(queue):
        x, y = queue.pop()
        seen.add((x,y))

        z = heightmap[y][x]
        if z == "9":
            continue
              
        size += 1
        nbs = get_neighbors(x, y, heightmap) - seen
        queue = queue | nbs
    return size



def get_neighbors(x,y,hm):
    max_x = len(hm[0]) - 1
    max_y = len(hm) - 1

    nb = set()

    if x > 0:
        nb.add((x-1, y))

    if x < max_x:
        nb.add((x+1, y))

    if y > 0:
        nb.add((x, y-1))

    if y < max_y:
        nb.add((x, y+1))

    return nb




if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')