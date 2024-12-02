# gamma rate = for each bit, most common value
# epsilon rate = for each bit, least common value = NOT(gamma)
# gamma * epsilon = power consumption

NUM_BITS = 12

def read_input() -> list[str]:
    with open("input.txt") as f:
        return [line.strip() for line in f.readlines()]


def determine_gamma(data: list[str]) -> int:
    bit_len = len(data[0])
    
    gamma_sums = [sum(int(bit[i]) for bit in data) >= 0.5 * len(data) for i in range(bit_len)]

    gamma_bits = "".join([str(int(x)) for x in gamma_sums])
    gamma = int(gamma_bits, 2)

    return gamma


def determine_epsilon(gamma: int) -> int:
    return ~gamma & ((1 << NUM_BITS) - 1)


def part_one():    
    bits = read_input()
    gamma = determine_gamma(bits)
    epsilon = determine_epsilon(gamma)

    return gamma * epsilon


def part_two():
    bits = read_input()

    oxy = filter_bits(bits, True)
    co2 = filter_bits(bits, False)

    assert oxy
    assert co2

    print(oxy, co2)

    return oxy * co2


def filter_bits(bits: list[str], most_frequent=True):
    for i in range(NUM_BITS):
        num_1s = sum(int(x[i]) for x in bits)
        num_0s = len(bits) - num_1s
        
        if most_frequent:
            keep_bit = '1' if num_1s >= num_0s else '0'
        else:
            keep_bit = '0' if num_1s >= num_0s else '1'
        
        bits = [x for x in bits if x[i] == keep_bit]

        if len(bits) == 1:
            val = int("".join(bits[0]), 2)
            return(val)


def bin_str(x: int) -> str:
    return "{0:b}".format(x)


if __name__ == "__main__":
    instructions = read_input()
    
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')