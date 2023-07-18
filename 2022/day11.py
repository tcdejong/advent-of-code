import re
import logging
logging.basicConfig()
logging.root.setLevel(logging.INFO)
logger = logging.getLogger("day11")

PATTERN = r"Monkey (?P<num>\d+):\n.+items:.(?P<items>.+)\n.+: (?P<operation>.+)\n.+Test: (?P<test>.+)\n.+(?P<iftrue>\d)\n.+(?P<iffalse>\d)"

def read_input(filename: str = 'day11.txt'):
    with open(filename) as f:
        data = f.read()

    regexed_monkeys = re.findall(PATTERN, data)

    monkeys= [Monkey(matchgroup) for matchgroup in regexed_monkeys]
    # provide references to each other
    for monkey in monkeys:
        monkey.monkeys = monkeys

    return monkeys


class Monkey:
    monkeys: list['Monkey'] = []

    def __init__(self, regex_matches):
        self.name = int(regex_matches[0])
        self.items = [int(x) for x in regex_matches[1].split(', ')]
        self.operation: str = regex_matches[2]
        self.test: str = regex_matches[3]
        self.iftrue = int(regex_matches[4])
        self.iffalse = int(regex_matches[5])

        self.divisor = int(self.test[13:])
        self.num_inspections = 0
        self.monkeys.append(self)
        self.relaxation_factor = 3
        self.part = 1

    
    def take_turn(self):
        logger.debug(f'{self}:')

        
        while self.items:
            worrylevel = self.items.pop(0)
            logger.log(10,f'\tInspecting item {worrylevel=}')

            new_worrylevel = self.run_operation(worrylevel)

            recipient = self.run_test(new_worrylevel)
            logger.log(10,f'\t\t{recipient=} ({self.iftrue=})')


            self.monkeys[recipient].items.append(new_worrylevel)



    def run_operation(self, worrylevel: int):
        """Operation shows how your worry level changes as that monkey inspects an item. """
        assert self.operation.startswith('new = old ')

        self.num_inspections += 1
        operator = self.operation[10]
        operand = worrylevel if self.operation[12:] == 'old' else int(self.operation[12:])


        if operator == '+':
            new_worrylevel = worrylevel + operand
            logger.log(10,f'\t\t{worrylevel=} increases by {operand} to {new_worrylevel}')
        elif operator == '*':
            new_worrylevel = worrylevel * operand
            logger.log(10,f'\t\t{worrylevel=} is multiplied by {operand} to {new_worrylevel}')

        else:
            raise NotImplementedError()
        
        if self.part == 1:
            new_worrylevel = new_worrylevel // self.relaxation_factor
            logger.log(10,f'\t\tWorry level is divided by {self.relaxation_factor} and rounded down to {new_worrylevel}')

        return new_worrylevel


    def run_test(self, worrylevel: int):
        """Test shows how the monkey uses your worry level to decide where to throw an item next. """
        assert self.test.startswith('divisible by ')
        
        recipient = self.iftrue if worrylevel % self.divisor == 0 else self.iffalse
        return recipient
    

    def reduce_worrylevels(self, modulo):
        self.items = [wl % modulo for wl in self.items]
        

    def __repr__(self) -> str:
        return f"Monkey {self.name}"


def perform_round(monkeys: list[Monkey]):
    for monkey in monkeys:
        monkey.take_turn()


def part_one(monkeys: list[Monkey]):
    for i in range(20):
        perform_round(monkeys)
        logger.info(f'After round {i+1}, monkeys are holding these worry levels:')
        for m in monkeys:
            logger.info(f'{m}: {m.items}')

    monkeys_by_activity = sorted(monkeys, key=lambda m: m.num_inspections, reverse=True)
    return monkeys_by_activity[0].num_inspections * monkeys_by_activity[1].num_inspections


def part_two(monkeys: list[Monkey]):
    divisors = [m.divisor for m in monkeys]
    from math import lcm
    monkey_lcm = lcm(*divisors)

    for m in monkeys:
        m.part = 2
    
    for i in range(10_000):
        perform_round(monkeys)
        for m in monkeys:
            m.reduce_worrylevels(monkey_lcm)

        logger.info(f'Round {i+1} finished')
        for m in monkeys:
            logger.debug(f'{m}: {m.items}')

    monkeys_by_activity = sorted(monkeys, key=lambda m: m.num_inspections, reverse=True)
    return monkeys_by_activity[0].num_inspections * monkeys_by_activity[1].num_inspections    


if __name__ == '__main__':
    ex1 = read_input('day11ex1.txt')
    puzzle_input = read_input()
    # print(f'Part one: {part_one(puzzle_input)}')
    print(f'Part two: {part_two(puzzle_input)}')