from collections import namedtuple
from math import ceil, prod

PTYPE_SUM = 0
PTYPE_MUL = 1
PTYPE_MIN = 2
PTYPE_MAX = 3
PTYPE_LITERAL = 4
PTYPE_GT = 5
PTYPE_LT = 6
PTYPE_EQ = 7

Packet = namedtuple("Packet", ['version', 'type', 'value', 'binstr'])


def read_input(filename: str = 'day16.txt'):    
    with open(filename) as f:
        data = f.read().strip()

    return data


def hexstr2binstr(chars: str):
    return "".join("{0:b}".format(int(c, 16)).rjust(4,'0') for c in chars)


def read_packet(binstr: str):
    if len(binstr) < 6:
        raise ValueError('binstr too short!')

    bin_version = binstr[:3]
    bin_type = binstr[3:6]

    packet_version = int(bin_version,2)
    packet_type = int(bin_type, 2)

    read_func = read_literal if packet_type == PTYPE_LITERAL else read_operator
    packet, remainder = read_func(binstr, packet_version, packet_type)
    
    return packet, remainder


def read_literal(binstr, packet_version, packet_type):
    data_bits = binstr[6:]
    block_width = 5
    num_blocks = ceil(len(data_bits) / block_width)
    i = -1
    
    data = ""
    for block in range(num_blocks):
        i = block * block_width
        j = i + block_width
        group = data_bits[i:j]
        data += group[1:]
        if group.startswith("0"):
            break
    
    length = 6 + i + block_width
    value = int(data,2)

    return Packet(packet_version, packet_type, value, binstr[:length]), binstr[length:]

    
def read_operator(binstr, packet_version, packet_type):
    length_type_id = binstr[6]
    mode = 'numbits' if length_type_id == "0" else 'numpackets'
    type_length = 15 if mode == 'numbits' else 11

    subpacket_len_bits = binstr[7:7+type_length]
    subpacket_len = int(subpacket_len_bits,2)

    payload = binstr[7+type_length:]
    numbits = 0
    numpackets = 0
    processed = 0
    data = []


    while processed < subpacket_len:
        packet, payload = read_packet(payload)
        data.append(packet)

        numbits += len(packet.binstr)
        numpackets += 1

        processed = numbits if mode == 'numbits' else numpackets
        if processed > subpacket_len:
            print('Warning! processed > subpacket_len')

    packet_len = 7+type_length+numbits
    p = Packet(packet_version, packet_type, data, binstr[:packet_len])

    return p, payload


def sum_of_version_numbers(packet: Packet):
    if isinstance(packet.value, int):
        return packet.version
    else:
        return packet.version + sum(sum_of_version_numbers(p) for p in packet.value)


def resolve_packet(packet: Packet) -> int:
    # If this is a literal, return its value
    if packet.type == PTYPE_LITERAL or isinstance(packet.value, int):
        return packet.value
    
    # If there are subpackets, resolve them first
    elif isinstance(packet.value, list):
        subpackets = packet.value
        sub_vals = [resolve_packet(p) for p in subpackets]

        if len(sub_vals) == 1: 
            return sub_vals[0]

        funcs = {
            PTYPE_SUM: sum,
            PTYPE_MUL: prod,
            PTYPE_MIN: min,
            PTYPE_MAX: max,
        }

        if packet.type in funcs:
            return funcs[packet.type](sub_vals)

        sub1, sub2 = sub_vals
        if packet.type == PTYPE_LT:
            return int(sub1 < sub2)
        
        if packet.type == PTYPE_GT:
            return int(sub1 > sub2)

        if packet.type == PTYPE_EQ:
            return int(sub1 == sub2)
    
    raise ValueError("Sanity check: Should never reach this...")
    

def part_one(hex_str:str|bool=False):

    if not hex_str:
        hex_str = read_input()

    assert isinstance(hex_str, str)

    binstr = hexstr2binstr(hex_str)
    packet, _ = read_packet(binstr)

    return sum_of_version_numbers(packet)


def part_two():
    hex_str = read_input()
    binstr = hexstr2binstr(hex_str)
    packet, _ = read_packet(binstr)

    return resolve_packet(packet)


if __name__ == '__main__':
    assert hexstr2binstr('D2FE28') == '110100101111111000101000'

    binstr = hexstr2binstr("D2FE28")
    packet, _ = read_packet(binstr)
    assert packet.value == 2021

    binstr = hexstr2binstr("38006F45291200")
    packet, _ = read_packet(binstr)
    assert len(packet.value) == 2
    assert len(packet.value[0].binstr) == 11
    assert packet.value[0].value == 10
    assert len(packet.value[1].binstr) == 16
    assert packet.value[1].value == 20


    binstr = hexstr2binstr("EE00D40C823060")
    packet, _ = read_packet(binstr)
    assert len(packet.value) == 3
    assert packet.value[0].value == 1
    assert packet.value[1].value == 2
    assert packet.value[2].value == 3

    assert part_one("8A004A801A8002F478") == 16

    # print('\n\n--------------------------------------\n\n')

    assert part_one("620080001611562C8802118E34") == 12
    assert part_one("C0015000016115A2E0802F182340") == 23
    assert part_one("A0016C880162017C3686B18A3D4780") == 31

    
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')

