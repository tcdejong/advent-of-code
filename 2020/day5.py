def part_one():
    data = read_input()
    ids = [read_partition(line) for line in data]
    res = max(ids)
    print(res)


def part_two():
    data = read_input()
    ids = set(read_partition(line) for line in data)
    
    min_id = 0
    max_id = read_partition('BBBBBBBRRR')

    for id in range(min_id + 1, max_id):
        if id in ids:
            continue

        if id - 1 in ids and id + 1 in ids:
            print(id)
            break



def read_input():
    with open("day5.txt") as file:
        return file.readlines()


def read_partition(partition: str):
    # F is lower half, B is upper half of rows 0-127
    # L is lower half, R is upper half of cols 0-7
    partition = partition.strip()
    
    if not partition:
        print(f'Ignoring {partition}...')
    
    row_search = [c == 'B' for c in partition[:7]]
    col_search = [c == 'R' for c in partition[7:]]

    row_search.reverse()
    col_search.reverse()

    row = sum(2**i for i, c in enumerate(row_search) if c)
    col = sum(2**i for i, c in enumerate(col_search) if c)

    id = row * 8 + col

    return id

    
assert read_partition('BFFFBBFRRR') == 567
assert read_partition('FFFBBBFRRR') == 119
assert read_partition('BBFFBBFRLL') == 820

assert read_partition('FFFFFFFLLL') == 0
assert read_partition('BBBBBBBRRR') == 1023


if __name__ == '__main__':
    part_one()
    part_two()