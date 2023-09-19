def read_input(filename: str = 'input.txt'):
    with open(filename) as f:
        data = [eval(line.strip()) for line in f.readlines() if line.strip() != '']

    pairs = list(zip(data[::2], data[1::2]))

    return pairs


def part_one(packet_pairs):
    sum_of_indices = 0

    for i, (left, right) in enumerate(packet_pairs, start=1):
        res = are_ordered_packets(left, right)
        if res:
            sum_of_indices += i

    return sum_of_indices


def are_ordered_packets(left_packet, right_packet):
    # print(f'Comparing {left_packet} vs {right_packet}')
    shortest_len = min(len(left_packet), len(right_packet))

    for i in range(shortest_len):
        l = left_packet[i]
        r = right_packet[i]
        l_is_int = isinstance(l, int)
        r_is_int = isinstance(r, int)

        # both are ints
        if l_is_int and r_is_int:
            # print(f'\tComparing {l} vs {r}')
            if l == r:
                # equal: look at next value
                continue
            
            return l < r

        # both are lists
        if not l_is_int and not r_is_int:
            res = are_ordered_packets(l, r)
            
            if res == None:
                continue
            
            return res
        
        # mixed: convert int to list
        # print(f'Mixed types, converting...')
        if l_is_int:
            l = [l]
        if r_is_int:
            r = [r]
        res = are_ordered_packets(l, r)
        if res == None:
            continue
        return res

    else: # loop exits normally, iterated all values
        if len(left_packet) != len(right_packet):
            # print('Exactly one list exhausted')
            return len(left_packet) < len(right_packet)
        else:
            # print('Both lists exhausted')
            return None
    
    raise ValueError   


def part_two(packet_pairs):
    """Sorted insertion"""
    divider_packets = ([[2]], [[6]])
    unsorted_packets = [packet for pair in packet_pairs for packet in pair]
    sorted_packets:list = [*divider_packets]

    while unsorted_packets:
        packet, unsorted_packets = unsorted_packets[0], unsorted_packets[1:]

        for i, sorted_packet in enumerate(sorted_packets):
            if not are_ordered_packets(sorted_packet, packet):
                sorted_packets.insert(i, packet)
                break
        else:
            sorted_packets.append(packet)

    divider_idx = [sorted_packets.index(d)+1 for d in divider_packets]
    return divider_idx[0] * divider_idx[1]



def run_extra_Tests():
    # Extra test cases from reddit 
    # https://www.reddit.com/r/adventofcode/comments/zmkls9/2022_day_13_part_1_python_more_test_cases_for/
    
    test_cases = [ 
        (([[1],[2,3,4]],[[1],4]),'smaller'),
        (([1,1,1],[1, 1]),'bigger'),
        (([[1],1],[1,1,1]),'smaller'),
        (([1,1],[1,1,1]),'smaller'),
        (([9],[8, 7, 6]),'bigger'),
        (([],[[]]),'smaller'),
        (([[[]]],[[]]),'bigger'),
        (([3],[[]]),'bigger'),
        (([[[3]]],[[3]]),'equal'),
        (([1,1,1],[1,1,1]),'equal'),
    ]

    for i, case in enumerate(test_cases, start=1):
        (l, r), correct_res = case
        if correct_res == 'equal':
            continue

        correct_res = True if correct_res == 'smaller' else False
        print(f'======TEST CASE {i}=======')
        test_res = are_ordered_packets(l, r)
        assert test_res == correct_res

if __name__ == '__main__':
    # ex_packet_pairs = read_input('ex1.txt')
    # assert part_one(ex_packet_pairs) == 13
    # assert part_two(ex_packet_pairs) == 140
   
    # run_extra_Tests()

    packet_pairs = read_input()
    print(f'Part one: {part_one(packet_pairs)}')
    print(f'Part two: {part_two(packet_pairs)}')