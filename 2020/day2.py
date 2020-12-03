def read_input():
    with open("day2.txt") as file:
        lines = file.readlines()
    
    return lines


def clean_line(line: str):
    line = line.strip()
    if not line:
        return False

    policy, letter, password = line.split(" ")

    a, b = policy.split("-")
    a = int(a)
    b = int(b)

    letter = letter[0]

    return (a, b, letter, password)


def is_valid_1(line: str) -> bool:
    pol_min, pol_max, letter, password = clean_line(line)
    occurrences = password.count(letter)

    return pol_min <= occurrences <= pol_max


def is_valid_2(line: str) -> bool:
    pos_a, pos_b, letter, password = clean_line(line)

    pos_a -= 1
    pos_b -= 1

    match1 = password[pos_a] == letter
    match2 = password[pos_b] == letter

    return (match1 or match2) and match1 != match2


def part_one():
    lines = read_input()
    valid_passwords = sum(is_valid_1(line) for line in lines)
    print(valid_passwords) 


def part_two():
    lines = read_input()
    valid_passwords = sum(is_valid_2(line) for line in lines)
    print(valid_passwords) 


if __name__ == '__main__':
    part_one()
    part_two()