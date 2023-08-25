def read_input(file_name="day08.txt"):
    with open(file_name) as file:
        return [line.strip() for line in file.readlines()]


def decoded_difference(line):
    decoded_line = bytes(line, "utf-8").decode("unicode_escape") 
    return len(line) - len(decoded_line) + 2 # account for the quotes


def encoded_difference(line):
    index = 0

    res = 4 + len(line)
    while index < len(line):
        c = line[index]

        if c == '\\':
            c2 = line[index + 1]

            if c2 == "x":
                res += 1
                index += 3
            else:
                res += 2
                index += 2
        else:
            index += 1

    return res - len(line)


def part_one():
    data = read_input()
    total_difference = sum(decoded_difference(line) for line in data)
    print(total_difference)


def part_two():
    data = read_input()
    total_difference = sum(encoded_difference(line) for line in data)
    print(total_difference)


if __name__ == '__main__':
    # part_one()
    part_two()