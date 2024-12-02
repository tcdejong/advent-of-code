from collections import namedtuple
from dataclasses import dataclass

MicroChip = namedtuple("MicroChip", "val target output") 
# val=value, target=id of bot/output, output distinguishes bot/outputs

def read_input(filename: str = 'input.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    bot_instructions = [line.split() for line in data if line.startswith('bot')]
    bots_sorted: list[Bot] = [None for _ in bot_instructions]

    for instr in bot_instructions:
        botnum = int(instr[1])
        low_target = instr[5]
        low_id = int(instr[6])
        high_target = instr[-2]
        high_id = int(instr[-1])

        bots_sorted[botnum] = Bot(low_target, low_id, high_target, high_id, set())

    microchips = [line.split() for line in data if line.startswith('value')]
    microchips = [MicroChip(int(splitline[1]), int(splitline[-1]), 'bot') for splitline in microchips]

    return bots_sorted, microchips


@dataclass
class Bot:
    low_out_or_bot: str
    low_target: int
    high_out_or_bot: str
    high_target: int
    held_vals: set

    def receive(self, val):
        self.held_vals.add(val)
        assert len(self.held_vals) <= 2

    def give(self):
        low, high = min(self.held_vals), max(self.held_vals)
        self.held_vals = set()
        return MicroChip(low, self.low_target, self.low_out_or_bot), MicroChip(high, self.high_target, self.high_out_or_bot)



def part_one(bots: list[Bot], values: list[MicroChip]):
    while values:
        val, values = values[0], values[1:]
        if val.output != 'bot':
            continue
        
        bot = bots[val.target]
        bot.receive(val.val)

        if len(bot.held_vals) == 2:
            if 61 in bot.held_vals and 17 in bot.held_vals:
                return val.target
            values.extend(bot.give())


def part_two(bots: list[Bot], values: list[MicroChip]):
    outputs = {}

    while values:
        val, values = values[0], values[1:]

        if val.output == 'output':
            assert val.target not in outputs
            outputs[val.target] = val.val
            continue
        
        bot = bots[val.target]
        bot.receive(val.val)

        if len(bot.held_vals) == 2:
            values.extend(bot.give())

        if 0 in outputs and 1 in outputs and 2 in outputs:
            break

    return outputs[0] * outputs[1] * outputs[2]


if __name__ == '__main__':
    bots, microchips = read_input()
    print(f'Part one: {part_one(bots, microchips)}')
    print(f'Part two: {part_two(bots, microchips)}')