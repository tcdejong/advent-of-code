from __future__ import annotations


def next_departure(search_time, bus_id):
    since_last_departure = search_time % bus_id
    return search_time if since_last_departure == 0 else bus_id - since_last_departure


def part_one():
    search_time, bus_ids = read_input()
    departures = [(bus_id, next_departure(search_time, bus_id)) for bus_id in bus_ids]
    earliest = min(departures, key=lambda x: x[1])

    print(f'Part one: {earliest[0]} * {earliest[1]} = {earliest[0] * earliest[1]}')


def pair_two(id1, id2, t0, offset, phase=None):
    """
    Find first t where:
        t >= t0
        id1 departs at t
        id2 departs at t+offset

    Take steps of size phase. Phase is the joint period of already matched buses.
    If this is the first match, it's the interval (id) of bus 1

    This is dark magic.
    """
    t = t0

    if not phase:
        phase = id1

    while not (t % id1 == 0 and (t+offset) % id2 == 0):
        t += phase

    phase = phase * id2
    return (t, phase)


def part_two():
    """
    Given bus ids [7,13,'x','x',59,'x',31,19],
    find t so that:
        bus 7 departs at t
        bus 13 at t+1
        ...                 no constraint at t+2 (x)
        ...                 at t+3 (x)
        bus 59 at t+4
        ...                 at t+5 (x)
        bus 31 at t+6
        bus 19 at t+7


        Ergo, find t so that:
        (t + 0) % 7 = 0
        (t + 1) % 13 = 0
        (t + 4) % 59 = 0
        (t + 6) % 31 = 0
        (t + 7) % 19 = 0

        relation (t+x) % y = 0 and t % y = z?
        (10+1) % 5 = 1
        10 % 5 = 0

        (9+1) % 5 = 0
        9 % 5 = 4
    """
    _, raw_bus_ids = read_input(raw=True)
    bus_and_offset = [(int(bus), i) for i, bus in enumerate(raw_bus_ids) if bus != 'x']

    # pair other busses one by one with bus 1, but keep track of phase for valid solutions.
    id1 = bus_and_offset[0][0]
    t0 = 0
    phase = 1
    for id2,offset in bus_and_offset[1:]:
        t0, phase = pair_two(id1, id2, t0, offset, phase)

    print('Part two:', t0)



def read_input(file_path = "day13.txt", raw=False):
    with open(file_path) as file:
        lines = file.readlines()
    
    search_time = int(lines[0])
    bus_ids = lines[1].split(',') if raw else [int(i) for i in lines[1].split(',') if i.isnumeric()]

    return search_time, bus_ids


