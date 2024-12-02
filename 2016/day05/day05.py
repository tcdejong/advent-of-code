from hashlib import md5


def crack_code_letter(door_id, idx, part_two=False):
    while True:
        hash_str = f'{door_id}{idx}'.encode()
        hashed = md5(hash_str).hexdigest()

        if hashed[:5] == '00000':

            if part_two:
                pos = hashed[5]
                if pos in '01234567':
                    pos = int(pos)
                    return pos, hashed[6], idx
                else:
                    idx += 1
            else:
                print(f'hit on {idx=}')
                return hashed[5], idx
        else:
            idx += 1




def part_one(door_id):
    idx = 0
    code = ""
    for _ in range(8):
        char, idx = crack_code_letter(door_id, idx)
        assert isinstance(char, str)
        assert isinstance(idx, int)

        code += char
        idx += 1

    return code


def part_two(door_id):
    idx = 0
    code = ['_' for _ in range(8)]
    while any(c == '_' for c in code):
        pos, char, idx = crack_code_letter(door_id, idx, True)
        assert isinstance(pos, int)
        assert isinstance(char, str)
        assert isinstance(idx, int)

        if code[pos] == '_':
            code[pos] = char
            print("".join(code))
        idx += 1

    return "".join(code)


if __name__ == '__main__':
    PUZZLE_INPUT = 'ugkcyxxp'

    # assert part_one("abc") == "18f47a30"

    # print(f'Part one: {part_one(PUZZLE_INPUT)}')
    print(f'Part two: {part_two(PUZZLE_INPUT)}')