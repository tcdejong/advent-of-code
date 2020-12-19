from math import prod


def next_departure(search_time, bus_id):
    since_last_departure = search_time % bus_id
    return search_time if since_last_departure == 0 else bus_id - since_last_departure


def part_one():
    search_time, bus_ids = read_input()

    departures = [(bus_id, next_departure(search_time, bus_id)) for bus_id in bus_ids]

    earliest = min(departures, key=lambda x: x[1])

    print(f'Part one: {earliest[0]} * {earliest[1]} = {earliest[0] * earliest[1]}')


def part_two_bf():
    _, raw_bus_ids = read_input(raw=True)

    # brute force: find t so that t+i % bus == 0 for all i != x

    # ex1 = [7,13,'x','x',59,'x',31,19] # 1068781
    # ex2 = [1789,37,47,1889] # 1202161486

    t = prod(int(i) for i in raw_bus_ids if i.isnumeric())

    while True:
        if all((t + i) % int(bus) == 0 for i, bus in enumerate(raw_bus_ids) if bus != 'x'):
            break
        
        if t % 1_000_000 == 0:
            print(f'{t/1_000_000=}...')
        
        t +=1 

    print(f'Part two: {t=}')


def part_two():
    _, raw_bus_ids = read_input(raw=True)
    # ex1 = [7,13,'x','x',59,'x',31,19] # 1068781
    # ex2 = [1789,37,47,1889]           # 1202161486

    bus_ids = [(i, int(bus)) for i, bus in enumerate(raw_bus_ids) if bus != 'x']

    # i, j = bus_ids[:2]

    # n = i[1]
    # while True:
    #     if n % i and (n+)
    #     n += i

    # t is valid if:
    # (t + i) % id == 0 for each bus id

    # print(f'Part two: {t=}')


def read_input(file_path = "day13.txt", raw=False):
    with open(file_path) as file:
        lines = file.readlines()
    
    search_time = int(lines[0])
    bus_ids = lines[1].split(',') if raw else [int(i) for i in lines[1].split(',') if i.isnumeric()]

    return search_time, bus_ids


# if __name__ == '__main__':
    # part_one()
    # part_two()
    # visualizer()

part_two()



