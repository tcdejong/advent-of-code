def read_input(filename: str = 'day06.txt'):
    with open(filename) as f:
        data = f.read().strip()

    return data


def part_one(puzzle_input, packet_length = 4):
    i=0
    for i, _ in enumerate(puzzle_input):
        if len(set(puzzle_input[i:i+packet_length])) == packet_length:
            break
    
    return i+packet_length
        

def part_two(puzzle_input):
    return part_one(puzzle_input, packet_length=14)


if __name__ == '__main__':

    assert part_one("bvwbjplbgvbhsrlpgdmjqwftvncz") == 5
    assert part_one("nppdvjthqldpwncqszvftbrmjlhg") == 6
    assert part_one("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg") == 10
    assert part_one("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw") == 11

    puzzle_input = read_input()
    print(f'Part one: {part_one(puzzle_input)}')
    print(f'Part two: {part_two(puzzle_input)}')