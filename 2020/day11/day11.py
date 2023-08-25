EMPTY = 'L'
FLOOR = '.'
OCCUPIED = '#'

ex1 = """
#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##
"""

ex2 = """
.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....
"""

ex3 = """
.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.
"""

ex4 = """
.............
.L.L.#.#.#.#.
.............
"""


def count_occupied_neighbors(seat_row, seat_col, grid):
    count = 0
    num_col = len(grid[0])

    from_col = max(seat_col-1, 0)
    to_col   = min(seat_col+1, num_col)

    from_row = max(seat_row-1, 0)
    to_row   = min(seat_row+1, len(grid))

    for line in grid[from_row:to_row+1]:
        count += line[from_col:to_col+1].count(OCCUPIED)

    if grid[seat_row][seat_col] == OCCUPIED:
        count -= 1

    return count


def count_occupied_seen(seat_row, seat_col, grid, verbose=False):
    count = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == dy == 0:
                continue
            is_occupied = is_occupied_directional(seat_row, seat_col, dx, dy, grid, verbose)
            count += is_occupied
    return count


def is_occupied_directional(seat_row, seat_col, dx, dy, grid, verbose=False):
    x = seat_col
    y = seat_row

    if verbose:
        print('direction:', dx, dy)

    while True:
        x, y = x+dx, y+dy

        if x < 0 or y < 0:
            return False

        try: 
            state = grid[y][x]
        except IndexError:
            return False

        if verbose:
            print(f'state at {x=}, {y=}:', state)

        if state == FLOOR:
            continue
        
        return state == OCCUPIED


def main(part=1):
    layout = read_input()

    new_layout = None
    count = 0

    while True:
        new_layout = [[new_state(row_num, col, layout, part) for col, _ in enumerate(row)] for row_num, row in enumerate(layout)]
        count += 1

        if new_layout == layout:
            break
        
        layout = new_layout

    total_occupied = sum(map(lambda line: line.count(OCCUPIED), layout))

    print(f'Steady configuration after {count} steps')
    print(f'{total_occupied} occupied seats')


def new_state(seat_row, seat_col, grid, part=1):
    seat = grid[seat_row][seat_col]

    if seat == FLOOR:
        return FLOOR

    if part == 1:
        occupied_neigbors = count_occupied_neighbors(seat_row, seat_col, grid)
    else:
        occupied_neigbors = count_occupied_seen(seat_row, seat_col, grid)

    if seat == OCCUPIED and ((occupied_neigbors >= 4 and part == 1) or (occupied_neigbors >= 5 and part == 2)):
        return EMPTY
    elif seat != OCCUPIED and occupied_neigbors == 0:
        return OCCUPIED

    return seat


def parse_layout(grid_string:str):
    grid = [list(line.strip()) for line in grid_string.strip().splitlines()]
    # [print(i, line) for i, line in enumerate(grid)]

    return grid


def read_input():
    with open('day11.txt') as f:
        return parse_layout(f.read())




main(part=1)
main(part=2)

