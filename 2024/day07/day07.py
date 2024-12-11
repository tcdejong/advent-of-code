from functools import lru_cache
from itertools import permutations
from typing import Callable, Iterable, Sequence, NewType, TypeAlias
from math import prod
from multiprocessing import Pool

Goal = NewType("Goal", int)
Parameters = NewType("Parameters", list[int])
Instruction = NewType("Instruction", tuple[Goal, Parameters])
Operation: TypeAlias = Callable[[Sequence[int]], int]


def read_input(filename: str = "input.txt"):
    with open(filename) as f:
        data = [clean_input_line(line) for line in f.readlines()]

    data: list[Instruction]
    return data


def clean_input_line(line: str):
    goal, params = line.strip().split(":")
    goal = int(goal)
    params = tuple(int(x) for x in params.split())

    instr: Instruction = (goal, params)

    return instr


def has_solution(goal: int, params: list[int], allowed_operations: Sequence[Operation]):
    num_params = len(params)

    if num_params == 1:
        return goal == params[0]

    new_params = [[x if i != 0 else op(params[:2]) for i, x in enumerate(params[1:])] for op in allowed_operations]
    return any(has_solution(goal, p, allowed_operations) for p in new_params)


def concat(vals: Iterable[int]):
    return int("".join(str(x) for x in vals))


def part_one(instructions: Iterable[Instruction]) -> int:
    valid_instructions = (inst for inst in instructions if has_solution(*inst, [prod, sum]))
    return sum(goal for goal, _ in valid_instructions)


def part_two(instructions: Iterable[Instruction]):
    valid_instructions = (inst for inst in instructions if has_solution(*inst, [prod, sum, concat]))
    return sum(goal for goal, _ in valid_instructions)


if __name__ == "__main__":
    puzzle_input = read_input()
    example_input = read_input("ex1.txt")
    longest_instruction = max(len(x[1]) for x in puzzle_input)
    
    
    assert part_one(example_input) == 3749
    print(f"Part one: {part_one(puzzle_input)}")
    

    assert part_two(example_input) == 11387
    print(f'Part two: {part_two(puzzle_input)}')
