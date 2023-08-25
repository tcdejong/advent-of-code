import re


def read_input(filename: str = 'day7.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]
    return data


def supports_tls(address):
    # left, mid, right = re.split(r"\W", address)
    segments = re.split(r"\W", address)

    inside = segments[1::2]
    if any(includes_abba(segment) for segment in inside):
        return False
    
    outside = segments[0::2]
    if any(includes_abba(segment) for segment in outside):
        return True

    return False


def supports_ssl(address):
    # left, mid, right = re.split(r"\W", address)
    segments = re.split(r"\W", address)

    inside = segments[1::2]
    outside = segments[0::2]

    babs = (bab for segment in outside for bab in find_aba_as_bab(segment))
    return any(bab in segment for bab in babs for segment in inside)


def find_aba_as_bab(segment):
    res = set()

    for i in range(len(segment)):
        chars = segment[i:i+3]
        if len(chars) != 3:
            break

        if chars[0] != chars[1] and chars[0] == chars[2]:
            bab = "".join((chars[1], chars[0], chars[1]))
            res.add(bab)

    return res


def includes_abba(segment):
    for i in range(len(segment)):
        chars = segment[i:i+4]
        if len(chars) != 4:
            break

        if chars[0] != chars[1] and chars[0] == chars[3] and chars[1] == chars[2]:
            return True

    return False


def part_one(adresses):
    return sum(supports_tls(adr) for adr in adresses)


def part_two(adresses):
    return sum(supports_ssl(adr) for adr in adresses)


if __name__ == '__main__':
    adresses = read_input()

    # asserts part one
    assert supports_tls('abba[mnop]qrst') == True
    assert supports_tls('abcd[bddb]xyyx') == False
    assert supports_tls('aaaa[qwer]tyui') == False
    assert supports_tls('ioxxoj[asdfgh]zxcvbn') == True
    
    assert supports_tls('abba[asdf]abba') == True
    assert supports_tls('cccc[asdf]abba') == True

    # asserts part two
    assert supports_ssl('aba[bab]xyz') == True
    assert supports_ssl('xyx[xyx]xyx ') == False
    assert supports_ssl('aaa[kek]eke') == True
    assert supports_ssl('zazbz[bzb]cdb') == True

    assert supports_ssl('aba[aba]fff[bab]xyz') == True

    print(f'Part one: {part_one(adresses)}')
    print(f'Part two: {part_two(adresses)}')