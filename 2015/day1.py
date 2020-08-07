def part_one():
    floor = 0
    for char in puzzle_input:
        if char == "(": 
            floor += 1

        elif char == ")":
            floor -= 1
    
    print(f"Pt1: {floor}")


def part_two():
    floor = 0
    for i, char in enumerate(puzzle_input):
        if char == "(": 
            floor += 1

        elif char == ")":
            floor -= 1

        if floor < 0:
            print(f"Pt2: {i + 1}")
            break


if __name__ == "__main__":
    with open("day1.txt") as file:
        puzzle_input = file.readline()
    
    part_one()
    part_two()