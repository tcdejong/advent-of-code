def part_one(puzzle_input):
    x, y = 0, 0
    received_gift = set()
    received_gift.add((x,y))

    for direction in puzzle_input:
        x, y = pos_after_step(x,y,direction)
        received_gift.add((x, y))

    print(f"Pt1: {len(received_gift)}")


def part_two(puzzle_input):
    x1, y1 = 0, 0
    x2, y2 = 0, 0
    received_gift = set()
    received_gift.add((x1,y1))
    robo_moves = True

    for direction in puzzle_input:
        if robo_moves:
            x1, y1 = pos_after_step(x1, y1, direction)
            latest = (x1, y1)
        else:
            x2, y2 = pos_after_step(x2, y2, direction)
            latest = (x2, y2)

        robo_moves = (not robo_moves)
        received_gift.add(latest)

    print(f"Pt2: {len(received_gift)}")


def pos_after_step(x, y, direction):
    if direction == "^":
        y += 1
    elif direction == ">":
        x += 1
    elif direction == "v":
        y -= 1
    elif direction == "<":
        x -= 1

    return (x,y)



if __name__ == "__main__":
    # convert puzzle input into list of (w,h,l) integer tuples
    with open("day3.txt") as file:
        puzzle_input = list(file.readline())

    part_one(puzzle_input)
    part_two(puzzle_input)