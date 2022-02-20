def read_input(filename: str = 'day13.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines() if line.strip()]

    dots = [line for line in data if line[0].isnumeric()]
    dots = [line.split(',') for line in dots]
    dots = set([tuple(int(x) for x in dot) for dot in dots])
    folds = [line.replace('fold along ', '').partition('=') for line in data if line[0] == "f"]
    return dots, folds


def fold_dot(dot: tuple[int, int], fold: tuple[str, str, str]) -> tuple[int,int]:
    axis = fold[0]
    fold_at = int(fold[2])
    x,y = dot

    return (x,fold_at - abs(fold_at-y)) if axis == 'y' else (fold_at - abs(fold_at - x), y)


def print_dots(dots: set[tuple[int,int]]) -> None:
    maxx = max(dots, key=lambda d: d[0])[0]
    maxy = max(dots, key=lambda d: d[1])[1]

    for y in range(maxy + 1):
        row = "".join(["#" if (x,y) in dots else " " for x in range(maxx + 1)])
        print(row)


def part_one():
    dots, folds = read_input()

    fold = folds[0]
    dots = set([fold_dot(dot, fold) for dot in dots])

    return len(dots)


def part_two():
    dots, folds = read_input()

    for fold in folds:
        dots = set([fold_dot(dot, fold) for dot in dots])

    print_dots(dots)


if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')


# ...#..#..#. 0
# ....#...... 1
# ........... 2
# #.......... 3 
# ...#....#.# 4
# ........... 5
# ........... 6     -> 6 = 7-abs(7-6)
# ----------- 7     -> 7
# ........... 8     -> 6
# ........... 9     -> 5 = 7-abs(7-9)
# .#....#.##. 10
# ....#...... 11
# ......#...# 12
# #.......... 13
# #.#........ 14


# fold along y=7


# #.##..#..#.
# #...#......
# ......#...#
# #...#......
# .#.#..#.###
# ...........
# ...........