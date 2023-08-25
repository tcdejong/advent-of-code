from itertools import islice

def is_preamble_sum(preamble, summed):
    partials = set()
    for num in preamble:
        if num in partials:
            return True

        partials.add(summed - num)
    
    return False


def part_one():
    data = read_input()
    
    max_i = len(data) - 26

    for i in range(max_i):
        preamble, summed = data[i:i+25], data[i+25]
        if not is_preamble_sum(preamble, summed):
            print(f'Part One, first invalid number: {summed}')
            return summed


def part_two(target):
    data = read_input()
    data = [x for x in data if x < target]
    
    # sliding window: 
    # If too low, move left pointer left
    # If too high, move right left
    # start with both pointers at the end

    left = 0
    right = 0
    observed_pointers = set()

    while (left, right) not in observed_pointers:
        observed_pointers.add((left, right))
        window = data[left:right+1]
        result = sum(window)

        if result == target:
            print(f'Part Two: {min(window) + max(window)}')


        elif result > target:
            left += 1
        
        elif result < target:
            right += 1


def read_input():
    with open("day9.txt") as file:
        return [int(num) for num in file.readlines()]


if __name__ == '__main__':
    target = part_one()
    part_two(target)
