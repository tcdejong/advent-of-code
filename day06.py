from collections import Counter

def read_input(filename: str = 'day6.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    return data


def part_one(messages):
    message_len = len(messages[0])

    counters = [Counter() for _ in range(message_len)]

    for message in messages:
        for pos, char in enumerate(message):
            counters[pos].update(char)

    reconstructed_msg = "".join(counter.most_common(1)[0][0] for counter in counters)
    return reconstructed_msg


def part_two(messages):
    message_len = len(messages[0])

    counters = [Counter() for _ in range(message_len)]

    for message in messages:
        for pos, char in enumerate(message):
            counters[pos].update(char)

    reconstructed_msg = "".join(counter.most_common()[-1][0] for counter in counters)
    return reconstructed_msg


if __name__ == '__main__':
    messages = read_input()
    print(f'Part one: {part_one(messages)}')
    print(f'Part two: {part_two(messages)}')