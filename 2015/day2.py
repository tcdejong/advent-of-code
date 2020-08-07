def paper_required(w,h,l):
    return 2*l*w + 2*w*h + 2*h*l + min(l*w, w*h, h*l)


def ribbon_required(w,h,l):
    min_perimeter = 2*(w+h+l)-2*max(w,h,l)
    volume = w*h*l
    return min_perimeter + volume


def part_one():
    res = 0
    for dims in puzzle_input:
        w,h,l = dims
        res += paper_required(w,h,l)

    print(f"Pt1: {res}")


def part_two():
    res = 0
    for dims in puzzle_input:
        w,h,l = dims
        res += ribbon_required(w,h,l)

    print(f"Pt2: {res}")


if __name__ == "__main__":
    # convert puzzle input into list of (w,h,l) integer tuples
    with open("day2.txt") as file:
        puzzle_input = [line.strip().split("x") for line in file.readlines()[:-1]]
        puzzle_input = [tuple(map(int, _)) for _ in puzzle_input]

    part_one()
    part_two()