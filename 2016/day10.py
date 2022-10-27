from collections import namedtuple
from dataclasses import dataclass

BotOutputs = namedtuple("BotOutputs", "bot low high output")
StartValue = namedtuple("StartValue", "val bot output")

def read_input(filename: str = 'day10.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    bots = [line.split() for line in data if line.startswith('bot')]
    bots = [BotOutputs(int(splitline[1]), int(splitline[6]), int(splitline[-1])) for splitline in bots]
    bots_sorted = [None for _ in bots]
    for bot in bots:
        bots_sorted[bot.bot] = Bot(bot.low, bot.high, set())

    values = [line.split() for line in data if line.startswith('value')]
    values = [StartValue(int(splitline[1]), int(splitline[-1])) for splitline in values]

    return bots_sorted, values


@dataclass
class Bot:
    out_low: int
    out_high: int
    held_vals: set

    def receive(self, val):
        self.held_vals.add(val)
        assert len(self.held_vals) <= 2

    def give(self):
        low, high = min(self.held_vals), max(self.held_vals)
        self.held_vals = set()
        return StartValue(low, self.out_low), StartValue(high, self.out_high)



def part_one(bots: list[Bot], values: list[StartValue]):
    while values:
        val, values = values[0], values[1:]
        bot = bots[val.bot]
        bot.receive(val.val)

        if len(bot.held_vals) == 2:
            if 61 in bot.held_vals and 17 in bot.held_vals:
                return val.bot
            values.extend(bot.give())


def part_two(puzzle_input):
    pass


if __name__ == '__main__':
    bots, values = read_input()
    print(f'Part one: {part_one(bots, values)}')
    # print(f'Part two: {part_two(puzzle_input)}')