""" 
Day 1 of Advent of Code's 2021 edition. 

Status:
    Part 1:  Done
    Part 2: 

"""

from typing import Iterable


def read_input() -> Iterable:
    with open("day1.txt") as f:
        return [int(line) for line in f.readlines()]


def part_one(depths: list[int]) -> int:
    num_increments = sum(a < b for a, b in zip(depths, depths[1:]))
    return num_increments


def part_two(depths: list[int]) -> int:
    window_size = 4
    last_window_idx = len(depths) - window_size + 1
    return sum(sum(depths[i:i+3]) < sum(depths[i+1:i+4])  for i in range(last_window_idx))


if __name__ == '__main__':
    depths = read_input()
    print(f'Part one: {part_one(depths)}')
    print(f'Part two: {part_two(depths)}')



# 0     199  A      
# 1     200  A B    
# 2     208  A B C  
# 3     210    B C D
# 4     200  E   C D
# 5     207  E F   D
# 6     240  E F G  
# 7     269    F G H
# 8     260      G H
# 9     263        H