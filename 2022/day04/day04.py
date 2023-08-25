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
    return any(seg1.l <= seg2.l and seg1.r >= seg2.r for (seg1, seg2) in [segments, segments[::-1]]) 


def overlap(segments):
    seg1, seg2 = segments
    return seg1.l <= seg2.l <= seg1.r or seg2.l <= seg1.l <= seg2.r


def part_one(puzzle_input):
    return sum(fully_contains(segments) for segments in puzzle_input)


def part_two(puzzle_input):
    return sum(overlap(segments) for segments in puzzle_input)


if __name__ == '__main__':
    segs = parse_segments("2-8,3-7")
    assert fully_contains(segs)
    
    segs = parse_segments("2-3,4-5")
    assert fully_contains(segs) == False

    puzzle_input = read_input()
    print(f'Part one: {part_one(puzzle_input)}')
    print(f'Part two: {part_two(puzzle_input)}')