def read_input():
    with open("day1.txt") as f:
        return [int(line) for line in f.readlines()]


def part_one(depths: list[int]) -> int:
    num_increments = sum(a < b for a, b in zip(depths, depths[1:]))
    return num_increments


def part_two(depths: list[int]) -> int:
    window_size = 4
    last_window_idx = len(depths) - window_size + 1
    return sum(sum(depths[i:i+3]) < sum(depths[i+1:i+4])  for i in range(last_window_idx))


if __name__ == '__main__':
    depths = read_input()
    print(f'Part one: {part_one(depths)}')
    print(f'Part two: {part_two(depths)}')
