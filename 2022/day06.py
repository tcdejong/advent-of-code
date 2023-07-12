def read_input(filename: str = 'day06.txt'):
    with open(filename) as f:
        data = f.read().strip()

    return data


def part_one(puzzle_input):
    for i, _ in enumerate(puzzle_input):
        if len(set(puzzle_input[i:i+4])) == 4:
            break
    
    return i+4
        
        
def part_two(puzzle_input):
    pass


if __name__ == '__main__':

    assert part_one("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert part_one("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert part_one("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert part_one("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

    puzzle_input = read_input()
    print(f'Part one: {part_one(puzzle_input)}')
    # print(f'Part two: {part_two(puzzle_input)}')