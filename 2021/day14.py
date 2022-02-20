from collections import Counter
import itertools
import pandas as pd
import numpy as np
from functools import reduce

Pair = tuple[str, str]

def read_input(filename: str = 'day14.txt'):
    with open(filename) as f:
        data = f.readlines()
    
    template = data[0].strip()
    rules = [line.partition(" -> ") for line in data[2:]]
    rules = [(rule[0], rule[2].strip()) for rule in rules]

    return template, rules


def polymer_insertion(polymer: str, rules: list) -> str:
    insertions: list[tuple[int, str]] = []

    for rule in rules:
        pair, element = rule
        indices = [(i+1, element) for i,_ in enumerate(polymer) if polymer[i:] and polymer[i:].startswith(pair)]
        insertions += indices

    insertions = sorted(insertions, key=lambda x: x[0])
    insertions = [(original_i + offset, x) for offset, (original_i, x) in enumerate(insertions)]

    for insertion in insertions:
        i, element = insertion
        polymer = polymer[:i] + element + polymer[i:]

    return polymer


def diff_maxmin_freq_after_n_iterations(n: int):
    """
    Brute-force application of polymer iteration rules.
    Possible optimization:
        Compress polymer as list of tuple[str,int], representing a character's repetitions.
        Insertions can only occur between tuples. 
    """
    polymer, rules = read_input()

    for _ in range(n):
        polymer = polymer_insertion(polymer, rules)

    counts = Counter(polymer)
    freq_min, freq_max = counts.most_common()[-1], counts.most_common()[0]

    return freq_max[1] - freq_min[1]


def part_one():
    return diff_maxmin_freq_after_n_iterations(10)


def part_two(iterations=40, polymer=None):
    # read insertion rules
    _polymer, rules = read_input() 

    if not polymer:
        polymer = _polymer

    # Determine all elements from the rules and input polymer
    # Generate a transition matrix
    mat = generate_pair_matrix(polymer, rules)
    mat = reduce(lambda a,b: a@b, (mat for _ in range(iterations)))

    # Turn starting polymer to state vector, with same format as transition matrix, then multiply
    state = polymer_to_state(polymer, mat.index)

    print(state.index)
    print(mat.index)
    print(mat.columns)

    new_state = state @ mat
    print(new_state.loc[new_state > 0])

    answer = state_to_answer(new_state, polymer)

    vars = {
        'answer': answer, 
        'mat': mat
    }
    return vars


def state_to_answer(state: pd.Series, starting_polymer):
    """Take the quantity of the most common element and subtract the quantity of the least common element"""
    print(state)

    # Retrieve all individual elements
    elements = set(char for key in state.index for char in key)

    # Determine counts per element
    counts = Counter()
    for element in elements:
        key_contains_element = [element in key for key in state.index]
        counts[element] += state.loc[key_contains_element].sum()

    # account for double-counting of all inner elements
    first_char = starting_polymer[0]
    last_char = starting_polymer[-1]

    print(f'{starting_polymer=}')

    counts[first_char] += 1
    counts[last_char] += 1
    for key, val in counts.items():
        counts[key] = val / 2

    sorted_counts = counts.most_common()
    print(sorted_counts)

    return int(sorted_counts[0][1] - sorted_counts[-1][1])


def generate_pair_matrix(polymer, rules):
    """
    Generate a state transition matrix from pair to pair
    E.g. 1 NN -> 1 NC + 1 CN
    E.g. 1 NB -> 1 NB
    """
    # Turn rules into a dict
    rule_dict = {tuple(pair): inserted for pair, inserted in rules}

    # Generate list of all used elements
    rule_chars = "".join(["".join(r) for r in rules])
    all_chars = "".join([*list(polymer), *list(rule_chars)])
    chars = set(all_chars)

    # Generate all possible pairs
    pairs = list(itertools.product(chars, repeat=2))

    # Generate empty transition matrix
    mat = pd.DataFrame(index=pairs, columns=pairs).fillna(0)
    mat = mat.convert_dtypes(np.uint64)

    # Fill transition matrix rows
    for pair in pairs:
        if pair not in rule_dict:
            mat.at[pair, pair] += 1
        
        else:
            inserted = rule_dict[pair]
            new_pairs = [(pair[0], inserted), (inserted, pair[1])]

            for newp in new_pairs:
                mat.at[pair, newp] += 1

    return mat


def polymer_to_state(polymer: str, index=pd.Index):
    state = pd.Series(index=index, dtype=int).fillna(0)
    polymer = list(polymer)

    for pair in zip(polymer, polymer[1:]):
        state.at[pair] += 1

    return state


if __name__ == '__main__':
    # print(f'Part one: {part_one()}')
    # print(f'Part two: {part_two(polymer = "NNCB", iterations=1)}')

    vars = part_two(polymer = "NNCB", iterations=1)

    for k,v in vars.items():
        print(k, v)

    # polymer, rules = read_input()
    # df = generate_pair_matrix(polymer, rules)

    # 2071495732310 => too low
