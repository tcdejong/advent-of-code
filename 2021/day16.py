from collections import namedtuple
from math import ceil

from rich.traceback import install
install(show_locals=True)


PTYPE_LITERAL = 4
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

    _, packet_type = read_version_and_id(binstr)
    
    if packet_type == PTYPE_LITERAL:
        packet = read_literal(binstr)
        return packet
    
    return read_operator(binstr)

    
def read_operator(binstr: str):
    packet_version, packet_type = read_version_and_id(binstr)
    length_type_id = binstr[6]
    mode = 'numbits' if length_type_id == "0" else 'numpackets'
    type_length = 15 if mode == 'numbits' else 11

    subpacket_len_bits = binstr[7:7+type_length]
    subpacket_len = int(subpacket_len_bits,2)

    subpacket_bits = binstr[7+type_length:]
    processed = 0
    data = []

    # print(f'\nReading operator packet')
    # print(f'{packet_version=}, {mode=}, {subpacket_len=}')
    # print(binstr)
    # print(binstr[:7])
    # print('       ', subpacket_len_bits, sep="")
    # print(subpacket_bits.rjust(len(binstr)), sep="")

    while processed < subpacket_len:
        packet = read_packet(subpacket_bits)
        data.append(packet)

        if mode == 'numbits':
            processed += len(packet.binstr)
        elif mode == 'numpackets':
            processed += 1
        else:
            raise ValueError()

        subpacket_bits = subpacket_bits[len(packet.binstr):]

        # [print('\t', d) for d in data]
        if processed > subpacket_len:
            print('Warning! processed > subpacket_len')

    p = Packet(packet_version, packet_type, data, binstr)

    return p


def read_version_and_id(binstr: str):
    bin_version = binstr[:3]
    bin_id = binstr[3:6]

    return int(bin_version,2), int(bin_id, 2)

    
def read_literal(binstr):
    packet_version, packet_type = read_version_and_id(binstr)
    # print(f'Reading literal packet {packet_version=} {binstr=}')
    data_bits = binstr[6:]
    block_width = 5
    num_blocks = ceil(len(data_bits) / block_width)
    # print(f'Literal packet, {data_bits=}')
    
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

    return Packet(packet_version, packet_type, value, binstr[:length])


def sum_of_version_numbers(packet: Packet):
    if isinstance(packet.value, int):
        return packet.version

    else:
        return packet.version + sum(sum_of_version_numbers(p) for p in packet.value)
    

def part_one(hex_str):
    binstr = hexstr2binstr(hex_str)
    packet = read_packet(binstr)

    print('Part one packet:')
    print(packet)

    return sum_of_version_numbers(packet)



def part_two():
    pass


if __name__ == '__main__':
    # assert hexstr2binstr('D2FE28') == '110100101111111000101000'
    # assert read_version_and_id('110100101111111000101000') == (6, 4)

    # binstr = hexstr2binstr("D2FE28")
    # packet = read_packet(binstr)
    # assert packet.value == 2021

    # binstr = hexstr2binstr("38006F45291200")
    # packet = read_packet(binstr)
    # assert len(packet.value) == 2
    # assert len(packet.value[0].binstr) == 11
    # assert packet.value[0].value == 10
    # assert len(packet.value[1].binstr) == 16
    # assert packet.value[1].value == 20


    # binstr = hexstr2binstr("EE00D40C823060")
    # packet = read_packet(binstr)
    # assert len(packet.value) == 3
    # assert packet.value[0].value == 1
    # assert packet.value[1].value == 2
    # assert packet.value[2].value == 3

    # assert part_one("8A004A801A8002F478") == 16

    # print('\n\n--------------------------------------\n\n')

    assert part_one("620080001611562C8802118E34") == 12
    
    # print(f'Part one: {part_one()}')
    # print(f'Part two: {part_two()}')

