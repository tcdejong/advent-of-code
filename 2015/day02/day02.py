def paper_required(w: int,h: int,l: int):
    area = (2*l*w) + (2*w*h) + (2*h*l)
    slack = min(l*w, w*h, h*l)
    return area + slack


def ribbon_required(w: int,h: int,l: int):
    min_perimeter = 2*(w+h+l)-2*max(w,h,l)
    volume = w*h*l
    return min_perimeter + volume


def part_one(puzzle_input: list[tuple[int, ...]]):
    res = 0
    for dims in puzzle_input:
        w,h,l = dims
        res += paper_required(w,h,l)

    print(f"Pt1: {res}")


def part_two(puzzle_input: list[tuple[int, ...]]):
    res = 0
    for dims in puzzle_input:
        w,h,l = dims
        res += ribbon_required(w,h,l)

    print(f"Pt2: {res}")


if __name__ == "__main__":
    # convert puzzle input into list of (w,h,l) integer tuples
    with open("input.txt") as file:
        puzzle_input = [line.strip().split("x") for line in file.readlines()]
        puzzle_input = [tuple(map(int, _)) for _ in puzzle_input]

    assert paper_required(2,3,4) == 58
    assert paper_required(1,1,10) == 43

    part_one(puzzle_input)
    part_two(puzzle_input)