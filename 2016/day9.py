def read_input(filename: str = 'day9.txt'):
    with open(filename) as f:
        data = f.read().strip()

    return data


def part_one(puzzle_input: str):
    decompressed_length = 0
    pointer = 0
    while pointer < len(puzzle_input):
        c = puzzle_input[pointer]

        if c != '(':
            decompressed_length += 1
            continue

        # We found an opening bracket. Now:
        # - Find matching closing bracket
        closing_bracket_idx = puzzle_input.find(')', pointer)
        
        # - Read the contained marker
        tag = puzzle_input[pointer+1:closing_bracket_idx]
        num_chars, repetitions = [int(i) for i in tag.split('x')]

        # - increment decompressed_length based on the number of reptitions
        decompressed_segment_length = num_chars * repetitions
        decompressed_length += decompressed_segment_length

        # - Jump forward past the repeated block
        pointer = closing_bracket_idx + num_chars + 1

    return decompressed_length





def part_two(puzzle_input):
    pass


if __name__ == '__main__':
    puzzle_input = read_input()
    print(f'Part one: {part_one(puzzle_input)}')
    # print(f'Part two: {part_two(puzzle_input)}')