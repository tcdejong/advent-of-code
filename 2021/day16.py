from collections import namedtuple
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

Packet = namedtuple("Packet", ['version', 'type', 'num_bits', 'value', 'binstr'])


def read_packet(binstr: str):

    # print(f'Reading packet: {binstr}')

    packet_version, packet_type = read_version_and_id(binstr)
    
    if packet_type == PTYPE_LITERAL:
        packet = read_literal(binstr)
        return packet
    
    return read_operator(binstr)

    
def read_operator(binstr: str):
    packet_version, packet_type = read_version_and_id(binstr)
    print(f'\nReading operator packet {packet_version=} {binstr=}')
    length_type_id = binstr[0]
    mode = 'numbits' if length_type_id == "0" else 'numpackets'
    type_length = 15 if length_type_id == "0" else 11


    subpacket_len_bits = binstr[7:7+type_length]
    subpacket_len = int(subpacket_len_bits,2)


    subpacket_bits = binstr[7+type_length:]
    print(f'{mode=}, {subpacket_bits=}')
    processed = 0
    data = []
    # print(f'Operator packet, {mode=}, {subpacket_len_bits=}, {subpacket_bits=}\n')
    while processed < subpacket_len:
        packet = read_packet(subpacket_bits)
        data.append(packet)

        subpacket_bits = subpacket_bits[len(packet.binstr):]

        if mode == 'numbits':
            processed += packet.num_bits
        elif mode == 'numpackets':
            processed += 1
        else:
            raise ValueError()

        if processed > subpacket_len:
            print('Warning! processed > subpacket_len')

    return Packet(packet_version, packet_type, "", data, binstr)


def read_version_and_id(binstr: str):
    bin_version = binstr[:3]
    bin_id = binstr[3:6]

    assert len(binstr) > 6

    return int(bin_version,2), int(bin_id, 2)

    
def read_literal(binstr):
    packet_version, packet_type = read_version_and_id(binstr)
    print(f'Reading literal packet {packet_version=} {binstr=}')
    data_bits = binstr[6:]
    block_width = 5
    num_blocks = ceil(len(data_bits) / block_width)

    # print(f'Literal packet, {data_bits=}')
    
    data = ""
    for block in range(num_blocks):
        i = block * block_width
        group = data_bits[i:i+block_width]
        data += group[1:]
        if group.startswith("0"):
            break
    
    length = 6 + i + block_width
    value = int(data,2)

    return Packet(packet_version, packet_type, length, value, binstr[:length])


def sum_of_version_numbers(packet: Packet):
    if isinstance(packet.value, int):
        return packet.version

    else:
        return sum(sum_of_version_numbers(p) for p in packet.value)
    



def part_one(hex_str):
    binstr = hexstr2binstr(hex_str)
    packet = read_packet(binstr)

    print(packet)

    return sum_of_version_numbers(packet)



def part_two():
    pass


if __name__ == '__main__':
    assert hexstr2binstr('D2FE28') == '110100101111111000101000'
    assert read_version_and_id('110100101111111000101000') == (6, 4)


    # print(f'Part one: {part_one()}')
    # print(f'Part two: {part_two()}')

    # USE_EX = True

    # hexstr = read_input(use_ex=USE_EX)

    # binstr = hexstr2binstr("D2FE28")
    # packets = read_packet(binstr)
    # print(packets)

    # binstr = hexstr2binstr("38006F45291200")
    # packets = read_packet(binstr)
    # print(packets)

    # binstr = hexstr2binstr("EE00D40C823060")
    # packets = read_packet(binstr)
    # print(packets)

    part_one("8A004A801A8002F478")


    

