from collections import namedtuple, Counter
from string import ascii_lowercase
from itertools import cycle, islice
RoomCode = namedtuple("RoomCode", "name id checksum")


def read_input(filename: str="day4.txt"):
    with open(filename) as f:
        codes = [read_roomcode(row) for row in f.readlines()]

    return codes


def read_roomcode(roomcode: str):
    name_id, checksum = roomcode.rsplit('[')
    name, room_id = name_id.rsplit('-', maxsplit=1)
    room_id = int(room_id)
    checksum = checksum.strip()[:-1]
    return RoomCode(name, room_id, checksum)


def is_real_room(room: RoomCode):
    name = room.name.replace('-', '')
    counts = list(sorted(Counter(name).most_common(), key=lambda x: (-x[1], x[0])))[:5]

    return all(
        c_counter == c_checksum for (c_counter, c_checksum) in zip(
        [c for (c, _) in counts],
        room.checksum
    ))


def decrypt_room(room: RoomCode):
    shift_by = room.id % 26
    words = room.name.replace('-', ' ')
    shifted = "".join(islice(cycle(ascii_lowercase), shift_by, shift_by+26))
    trans_table = str.maketrans(ascii_lowercase, shifted)

    return words.translate(trans_table)


def part_one(codes):
    return sum(room.id for room in codes if is_real_room(room))


def part_two(codes):
    for room in codes:
        decrypted_name = decrypt_room(room)
        if decrypted_name == 'northpole object storage':
            return room.id


def run_examples_pt1():
    examples = [
        ("aaaaa-bbb-z-y-x-123[abxyz]", True),
        ("a-b-c-d-e-f-g-h-987[abcde]", True),
        ("not-a-real-room-404[oarel]", True),
        ("totally-real-room-200[decoy]", False)
    ]

    for ex, val in examples:
        code = read_roomcode(ex)
        print(code)
        assert is_real_room(code) == val


if __name__ == '__main__':
    codes = read_input()
    print(f'Part one: {part_one(codes)}')
    print(f'Part two: {part_two(codes)}')