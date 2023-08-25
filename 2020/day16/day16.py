from math import prod

def read_input(fp = 'day16.txt'):
    with open(fp) as file:
        raw = file.read()

    raw_constraints, raw_my, raw_nearby = raw.split('\n\n')
    raw_constraints, raw_my, raw_nearby = raw_constraints.splitlines(), raw_my.splitlines()[-1], raw_nearby.splitlines()[1:]
    
    constraints = [read_constraint(constraint) for constraint in raw_constraints]
    my = read_ticket(raw_my)
    nearby = [read_ticket(line) for line in raw_nearby]

    return constraints, my, nearby


def read_constraint(line: str) -> tuple[str, tuple[int, int], tuple[int, int]]:
    # departure track: 40-626 or 651-952

    field, rest = line.split(':')
    range_a, range_b = rest.split(' or ')
    (a_min, a_max) = [int(x) for x in range_a.split('-')]
    (b_min, b_max) = [int(x) for x in range_b.split('-')]

    return (field, (a_min, a_max), (b_min, b_max))


def read_ticket(line: str) -> list[int]:
    return [int(x) for x in line.split(',')]


def invalid_ticket_numbers_sum(ticket, constraints):
    invalid_numbers = set()

    for number in ticket:
        for _, (a_min, a_max), (b_min, b_max) in constraints:
            if a_min <= number <= a_max or b_min <= number <= b_max:
               break
        else:
            invalid_numbers.add(number)
            
    return sum(invalid_numbers)


def part_one(tickets, constraints):
    result = sum(invalid_ticket_numbers_sum(ticket, constraints) for ticket in tickets)

    print(f'Part one: {result}')


def part_two(constraints, my, nearby):
    remaining_tickets = [ticket for ticket in nearby if invalid_ticket_numbers_sum(ticket, constraints) == 0 ]
    field_names = [name for (name, _, _) in constraints]

    invalid_number_idx = {field_name: set() for field_name in field_names}

    # Disqualify ticket number indices if an invalid value appears
    for ticket in remaining_tickets:
        for idx, number in enumerate(ticket):
            for field, (a_min, a_max), (b_min, b_max) in constraints:
                if not (a_min <= number <= a_max or b_min <= number <= b_max):
                    invalid_number_idx[field].add(idx)

    # Transform sets of invalid numbers to sets of valid numbers
    number_idx = set(range(len(my)))
    valid_number_idx = {field: number_idx - invalid_number_idx[field] for field in field_names}

    # Print results
    [print(f'{k:20}: {len(v):5} :  {v}') for k,v in valid_number_idx.items()]
    lengths = [len(v) for v in valid_number_idx.values()]
    lengths.sort()
    
    # Order fields in ascending order of remaining possible ticket number indices
    ordered_fields = {k:v for k, v in sorted(valid_number_idx.items(), key= lambda item: len(item[1]))}

    assigned_idx = set()
    field_idx = {}
    for field, options in ordered_fields.items():
        options = options - assigned_idx

        assert len(options) == 1

        idx = options.pop()
        field_idx[field] = idx
        assigned_idx.add(idx)


    # Calculate result
    indices = [field_idx[field] for field in field_names if field.startswith('departure')]
    result = prod(my[idx] for idx in indices)

    print(f'Part Two: {result}')
    

if __name__ == '__main__':
    # constraints, my, nearby = read_input('day16ex.txt')
    constraints, my, nearby = read_input()

    part_one(nearby, constraints)
    part_two(constraints, my, nearby)
