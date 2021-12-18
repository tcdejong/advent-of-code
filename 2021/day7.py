from collections import Counter

def read_input():
    with open("day7.txt") as f:
        data = map(int, f.read().split(','))
    return Counter(data)


def part_one():
    c = read_input()
    upper = max(c.keys())
    fuel_costs = (sum(abs(val - x) for val in c.elements()) for x in range(upper))
    pos,fuel = min(enumerate(fuel_costs), key=lambda kv: kv[1])
    return fuel


def fuel_cost(n):
    """
    Triangular numbers
    n      cost        
    0       0           0       
    1       1           1
    2       1 + 2       3
    3       1 + 2 + 3   6
    4       ... + 4     10
    """
    return (n+1)*n / 2


def part_two():
    c = read_input()
    upper = max(c.keys())
    fuel_costs = (sum(fuel_cost(abs(val - x)) for val in c.elements()) for x in range(upper))
    pos,fuel = min(enumerate(fuel_costs), key=lambda kv: kv[1])
    return int(fuel)


if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')