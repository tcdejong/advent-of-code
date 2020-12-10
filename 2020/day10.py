from collections import defaultdict
from pathlib import Path

def read_input():
    fp = Path('day10.txt')
    with open(fp) as file:
        return [int(i) for i in file.readlines()]


def part_one():
    adapters = read_input()
    adapters.sort()   
    jolts = [0, *adapters, adapters[-1]+3]

    differences = defaultdict(int)
    for i,j in zip(jolts[1:], jolts):
        differences[i-j] += 1

    print(differences[1] * differences[3])
    

def part_two():
    adapters = read_input()
    adapters.sort()

    jolts = [0, *adapters, adapters[-1] + 3]

    num_paths = [0 for _ in jolts]
    num_paths[0] = 1

    for i, jolt in enumerate(jolts):
        for j in range(1,4):
            if i+j >= len(jolts):
                continue 

            diff = jolts[i+j] - jolt
            if diff <= 3:
                num_paths[i+j] += num_paths[i]

    print(num_paths[-1])


if __name__ == '__main__':
    part_one()
    part_two()



