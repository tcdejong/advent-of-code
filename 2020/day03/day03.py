from math import prod

def read_input():
    with open("day3.txt") as file:
        grid = [line.strip() for line in file.readlines()]

    return grid


def count_trees(dx, dy):
    grid = read_input()
    x, y = 0, 0
    x_lim = len(grid[0])
    y_lim = len(grid)

    trees = 0

    while y < y_lim:
        trees += grid[y][x] == "#"
                
        x = (x + dx) % x_lim
        y += dy

    return trees


def part_one():
    print(count_trees(3,1))


def part_two():
    step_sizes = [
        (1, 1),
        (3, 1),
        (5, 1),
        (7, 1),
        (1, 2),
    ]

    trees = (count_trees(dx, dy) for (dx,dy) in step_sizes)

    print(prod(trees))



if __name__ == '__main__':
    part_one()
    part_two()