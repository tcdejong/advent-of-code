def read_input(filename: str = "input.txt"):
    with open(filename) as f:
        data = f.read().strip()

    return data


def part_one(diskmap: str):
    blockdata = expand_diskmap(diskmap)
    compacted = compact_diskmap(blockdata)
    checksum = calculate_checksum(compacted)
    return checksum


def part_two(diskmap: str):
    file_sizes = [x for x in diskmap[::2]]
    space_sizes = [x for x in diskmap[1::2]]
    block_starts = [sum(int(c) for c in diskmap[:i]) for i, _ in enumerate(diskmap)]

    files = [(int(size), start) for size, start  in zip(file_sizes, block_starts[::2])]
    spaces = [(int(size), start) for size, start  in zip(space_sizes, block_starts[1::2])]

    expanded = expand_diskmap(diskmap)

    for file_size, file_start in reversed(files):
        possible_spaces = [(i, space) for i, space in enumerate(spaces) if space[0] >= file_size and space[1] < file_start]

        if not possible_spaces:
            continue

        i, space = min(possible_spaces, key=lambda x: x[1][1])
        space_size, space_start = space

        expanded[space_start:space_start+file_size] = expanded[file_start:file_start+file_size]
        expanded[file_start:file_start+file_size] = ['.' for _ in range(file_size)]

        if space_size - file_size > 0:
            spaces[i] = (space_size - file_size, space_start + file_size)
        else:
            spaces.pop(i)
        
    checksum = calculate_checksum(expanded)
    return checksum


def compact_diskmap(diskmap: list[str]):
    assert diskmap[-1] != "."
    empty_spaces = sum(c == "." for c in diskmap)
    values_to_move = [c for c in diskmap[-empty_spaces:] if c.isnumeric()]
    compacted = [c if c.isnumeric() else values_to_move.pop() for c in diskmap[:-empty_spaces]]
    return compacted


def expand_diskmap(diskmap: str):
    blockdata = [str(i // 2) if i % 2 == 0 else "." for i, char in enumerate(diskmap) for _ in range(int(char))]
    return blockdata


def calculate_checksum(blocks: str | list[str]):
    if isinstance(blocks, str):
        blocks = list(blocks)
    return sum(i * int(c) for i, c in enumerate(blocks) if c.isnumeric())


if __name__ == "__main__":
    puzzle_input = read_input()
    example_input = "2333133121414131402"

    assert calculate_checksum(list("0099811188827773336446555566..............")) == 1928

    assert part_one(example_input) == 1928
    print(f"Part one: {part_one(puzzle_input)}")

    assert part_two(example_input) == 2858
    print(f'Part two: {part_two(puzzle_input)}')
