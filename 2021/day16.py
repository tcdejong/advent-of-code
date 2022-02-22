from dataclasses import dataclass
from math import ceil

# TODO: DECIDE between CLASS and FUNCTIONS
# TODO: Determine how to check/report back length of subpackets

def read_input(filename: str = 'day16.txt', *, use_ex=False):
    if use_ex:        
        return "D2FE28"
    
    with open(filename) as f:
        data = f.read().strip()

    return data


def hexstr2binstr(chars: str):
    return "".join("{0:b}".format(int(c, 16)).rjust(4,'0') for c in chars)


PTYPE_LITERAL = 4

@dataclass
class BITS:
    bits: str
    pointer = 0
    sum_of_versions = 0

    def __post_init__(self):
        if any(c not in {"0","1"} for c in self.bits):
            self.bits = hexstr2binstr(self.bits)


    def read_packet(self):
        packet_version, packet_type = self.read_version_and_id()

        self.sum_of_versions += packet_version
        
        if packet_type == PTYPE_LITERAL:
            return self.read_literal()

        type_length_id = binstr[0]


    def read_version_and_id(self):
        binstr = self.bits[self.pointer:]
        bin_version = binstr[:3]
        bin_id = binstr[3:6]
        self.pointer += 6
        return int(bin_version,2), int(bin_id, 2)

    
    def read_literal(self):
        block_width = 5
        num_blocks = ceil(len(self.bits) / block_width)
        
        data = ""
        for block in range(num_blocks):
            i = block * block_width
            group = self.bits[i:i+block_width]
            data += group[1:]

            if group.startswith("0"):
                break

        return data


# def read_bit_stream(binstr: str):
#     version, id = read_version_and_id(binstr)
#     bits = binstr[6:]

#     if id == 4:
#         return read_literal(bits)

#     type_length_id = binstr[0]

#     type_length = 15 if type_length_id == "0" else 11
#     bits = bits[type_length+1:]

#     print(bits)

#     # raise NotImplementedError()




    
#     return int(data,2)


def part_one():
    pass


def part_two():
    pass


if __name__ == '__main__':
    assert hexstr2binstr('D2FE28') == '110100101111111000101000'
    # assert read_version_and_id('110100101111111000101000') == (6, 4)

    bits = BITS('8A004A801A8002F478')
    bits.read_packet()
    print(bits.sum_of_versions)

    print(f'Part one: {part_one()}')
    # print(f'Part two: {part_two()}')

    USE_EX = True

    # hexstr = read_input(use_ex=USE_EX)
    # binstr = hexstr2binstr("38006F45291200")
    # res = read_bit_stream(binstr)
    # print(res)

