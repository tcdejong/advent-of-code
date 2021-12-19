import re
from dataclasses import dataclass

DIGITS = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg',
}

UNIQUE_LEN = {2,3,4,7}

SINGLE_BITS = [
    int('1000000',2),
    int('0100000',2),
    int('0010000',2),
    int('0001000',2),
    int('0000100',2),
    int('0000010',2),
    int('0000001',2),
]


def read_input(file="day8.txt"):
    with open(file) as f:
        data = f.read()

    mask = r"(\w+ \w+ \w+ \w+ \w+ \w+ \w+ \w+ \w+ \w+) [|] (\w+ \w+ \w+ \w+)"
    data = [tuple(x.split() for x in groups) for groups in re.findall(mask, data)]
    return data


def part_one():  
    data = read_input()
    output = [d[1] for d in data]
    out_count = sum(sum(len(x) in UNIQUE_LEN for x in out) for out in output)
    return out_count


         



def part_two():
    data = read_input()
    return sum(decode_output(entry) for entry in data)


def signal_to_bin(signal: str):
    """
    Convert string of characters a-g to 7bit mask.
    Each bit represents the enabled state of a wire.
    It is unknown which bit corresponds to which wire on the 7-segment display.
    """
    chars = 'abcdefg'
    bits = "".join('1' if char in signal else '0' for char in chars)
    return int(bits, 2)


def pat_to_bstr(pattern: int):
    """Format binary mask in human readable format. """
    return f"{pattern:07b}"


def decode_output(entry):
    """
    Follow predetermined strategy to decode all displays to their decimal values.
    """
    patterns, output = entry
    patterns = set(signal_to_bin(x) for x in patterns) # always 1-10 in random order
    output = [signal_to_bin(x) for x in output]

    wires = {}
    displays = {}


    # identify by length: 1, 4, 7, 8
    
    for pat in patterns:
        if pat.bit_count() == 2:
            displays[1] = pat
        elif pat.bit_count() == 3:
            displays[7] = pat
        elif pat.bit_count() == 4:
            displays[4] = pat
        elif pat.bit_count() == 7:
            displays[8] = pat

    # difference 7 and 1: wire a
    wires['a'] = displays[7] & ~displays[1]

    patterns = patterns - {v for v in displays.values()}



    # Remaining: 
    #   Displays 0, 2, 3, 5, 6, 9
    #   Segments b, c, d, e, f, g

    # display with all segments from 4, 7 and one unknown = 9, wire g + e

    req_wires = displays[4] | displays[7]
    # candidates = [pat for pat in patterns if (pat ^ req_wires).bit_count() == 1]
    candidates = [pat for pat in patterns if pat.bit_count() == 6 and (pat & ~req_wires).bit_count() == 1]
    assert len(candidates) == 1
    displays[9] = candidates[0]
    wires['g'] = displays[9] & ~displays[4] & ~displays[7]
    wires['e'] = displays[8] & ~displays[9]
    patterns = patterns - {displays[9]}


    # Remaining: 
    #   Displays 0, 2, 3, 5, 6
    #   Segments b, c, d, f

    # display with all segments on except 1 wire disabled from 1 = 6, wire c+f

    candidates = [pat for pat in patterns if pat.bit_count() == 6 and (pat & displays[1]).bit_count() == 1]
    assert len(candidates) == 1
    displays[6] = candidates[0]
    patterns = patterns - {displays[6]}

    wires['f'] = displays[6] & displays[1]
    wires['c'] = displays[1] & ~wires['f']


    # Remaining: 
    #   Displays 0, 2, 3, 5
    #   Segments b, d,

    # identify 0 by length (last with length 6), wire d

    candidates = [pat for pat in patterns if pat.bit_count() == 6]
    assert len(candidates) == 1
    displays[0] = candidates[0]
    patterns = patterns - {displays[0]}

    wires['d'] = displays[8] & ~displays[0]


    # Remaining: 
    #   Displays 2, 3, 5
    #   Segments b,

    # identify wire b from 4
    wires['b'] = displays[4] & ~displays[1] & ~wires['d']

    # fill in missing displays
    displays[2] = displays[8] & ~wires['b'] & ~wires['f']
    displays[3] = displays[8] & ~wires['b'] & ~wires['e']
    displays[5] = displays[8] & ~wires['c'] & ~wires['e']

    assert len(wires.values()) == len(set(wires.values()))
    assert len(displays.values()) == len(set(displays.values()))

    # decode output
    disp_inverted = {v: k for k, v in displays.items()}
    output_decimals = [str(disp_inverted[x]) for x in output]
    return int("".join(output_decimals))

    




if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')

    # data = read_input("day8.txt")
    # for line in data:
    #     print(decode_output(line))