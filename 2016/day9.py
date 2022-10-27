from collections import namedtuple
from math import prod

CharWeight = namedtuple("CharWeight", "weight end_pointer")

def read_input(filename: str = 'day9.txt'):
    with open(filename) as f:
        data = f.read().strip()

    return data


def find_decompressed_length(puzzle_input: str):
    decompressed_length = 0
    pointer = 0
    while pointer < len(puzzle_input):
        c = puzzle_input[pointer]

        if c != '(':
            decompressed_length += 1
            pointer += 1
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

        # - Jump forward
        pointer = closing_bracket_idx + num_chars + 1

    return decompressed_length



def find_decompressed_length2(puzzle_input: str):
    decompressed_length = 0
    pointer = 0
    
    char_weights = [CharWeight(1, len(puzzle_input)+1)]

    while pointer < len(puzzle_input):
        char_weights = [x for x in char_weights if x.end_pointer >= pointer]
        char_weight = prod(x.weight for x in char_weights)

        c = puzzle_input[pointer]

        if c != '(':

            decompressed_length += char_weight
            pointer += 1
            continue

        # We found an opening bracket. Now:
        # - Find matching closing bracket
        closing_bracket_idx = puzzle_input.find(')', pointer)
        
        # - Read the contained marker
        tag = puzzle_input[pointer+1:closing_bracket_idx]
        num_chars, repetitions = [int(i) for i in tag.split('x')]

        # - increment decompressed_length based on the number of reptitions
        decompressed_segment_length = num_chars * repetitions
        decompressed_length += decompressed_segment_length * char_weight

        # - Jump forward
        char_weights.append(CharWeight(repetitions, closing_bracket_idx + num_chars))
        pointer = closing_bracket_idx + 1


    return decompressed_length


def part_one(puzzle_input):
    return find_decompressed_length(puzzle_input)


def part_two(puzzle_input):
    return find_decompressed_length2(puzzle_input)


if __name__ == '__main__':
    puzzle_input = read_input()
    # print(f'Part one: {part_one(puzzle_input)}')
    print(f'Part two: {part_two(puzzle_input)}')

    # assert find_decompressed_length2('(3x3)XYZ') == 9
    print(find_decompressed_length2('X(8x2)(3x3)ABCY'), len('XABCABCABCABCABCABCY'))

    # 25381829764 too high
    