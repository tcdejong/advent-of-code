from dataclasses import dataclass

def read_input(filename: str = 'day10.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    return data

PIXEL_DARK = " "
PIXEL_LIGHT = "#"

@dataclass
class CRT:
    instructions: list[str]
    X: int = 1
    summed_sig_strength: int = 0
    display = [False for _ in range(240)]

    def run(self):
        cycle = 0
        hold = 0
        V = 0

        while self.instructions:
            cycle += 1
            self.read_signal_strength(cycle)
            self.draw_pixel(cycle)

            if hold == 1:
                self.X += V
            if hold > 0:
                hold -= 1
                continue

            inst = self.instructions.pop(0)
            if inst.startswith('addx'):
                V = int(inst.split()[-1])
                hold = 1

        print(f'{cycle=} \t {self.X=} \t {self.summed_sig_strength=}')

                

    def read_signal_strength(self, cycle):
        if self.should_read_signal_strength(cycle):
            self.summed_sig_strength += cycle * self.X
            # print(f'{cycle=} \t {self.X=} \t {self.summed_sig_strength=}')
    

    def draw_pixel(self, cycle):
        cycle = cycle-1
        if cycle % 40 in {self.X-1, self.X, self.X + 1}:
            self.display[cycle] = True


    def should_read_signal_strength(self, cycle):
        return cycle == 20 or (cycle - 20) % 40 == 0


    def print_display(self):
        disp = [PIXEL_LIGHT if p else PIXEL_DARK for p in self.display]
        for i in range(6):
            row = disp[i*40:(i+1)*40]
            print("".join(row))



def part_one(puzzle_input):
    crt = CRT(puzzle_input)
    crt.run()
    return crt.summed_sig_strength



def part_two(puzzle_input):
    crt = CRT(puzzle_input)
    crt.run()
    crt.print_display()


if __name__ == '__main__':
    puzzle_input = read_input()
    # puzzle_input = read_input('day10ex1.txt')
    # print(f'Part one: {part_one(puzzle_input)}')
    print(f'Part two: {part_two(puzzle_input)}')