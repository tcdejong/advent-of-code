from collections import namedtuple

Segment = namedtuple('Segment', 'l r')

def read_input(filename: str = 'day04.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    return [parse_segments(line) for line in data]


def parse_segments(raw_line): 
    raw_segments = raw_line.split(",")
    segments = [Segment(*[int(x) for x in seg.split('-')]) for seg in raw_segments]
    return segments


def fully_contains(segments):
    assert len(segments) == 2
    seg1, seg2 = segments
    seg1 = set(list(range(seg1.l, seg1.r+1)))
    seg2 = set(list(range(seg2.l, seg2.r+1)))

    return len(seg1 | seg2) == max(len(seg1), len(seg2))


def part_one(puzzle_input):
    return sum(fully_contains(segments) for segments in puzzle_input)


def part_two(puzzle_input):
    pass


if __name__ == '__main__':

    ex1 = read_input('day04ex1.txt')

    segs = parse_segments("2-8,3-7")
    assert fully_contains(segs)
    
    segs = parse_segments("2-3,4-5")
    assert fully_contains(segs) == False

    puzzle_input = read_input()
    print(f'Part one: {part_one(puzzle_input)}')
    # print(f'Part two: {part_two(puzzle_input)}')