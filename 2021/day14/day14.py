from collections import Counter, defaultdict
import itertools
import numpy as np
import pandas as pd
from functools import reduce


def read_input(filename: str = 'input.txt'):
    with open(filename) as f:
        data = f.readlines()
    
    template = data[0].strip()
    rules = [line.partition(" -> ") for line in data[2:]]
    rules = [(rule[0], rule[2].strip()) for rule in rules]

    return template, rules


def part_one():
    return day_14(iterations=10)


def part_two():
    return day_14(iterations=40)


def day_14(use_ex=False, iterations=40):
    input_name = 'ex1.txt' if use_ex else 'input.txt'
    polymer, rules = read_input(input_name) 

    # Determine all elements from the rules and input polymer
    # Generate a transition matrix
    mat = generate_pair_matrix(polymer, rules)
    mat = reduce(lambda a,b: a@b, (mat for _ in range(iterations)))

    # Turn starting polymer to state vector, with same format as transition matrix, then multiply
    state = polymer_to_state(polymer).reindex_like(mat.iloc[:, 0]).fillna(0)
    new_state = state @ mat

    answer = state_to_answer(new_state, polymer)

    return answer


def state_to_answer(state: pd.Series, starting_polymer):
    """Take the quantity of the most common element and subtract the quantity of the least common element"""

    # Retrieve all individual elements
    elements = set(char for key in state.index for char in key)

    # Determine counts per element by looking at pairs that start with it
    # eg for A include AB and AC, but not CA.
    # This will miss counting the very last element, because it doesn't appear at the start of a pair!
    counts = Counter()
    for element in elements:        
        include_pair = state.index.str.startswith(element)
        pairs = state.loc[include_pair]
        summed = pairs.sum()
        counts[element] += summed

    # compensate for missing the last element
    last_char = starting_polymer[-1]
    counts[last_char] += 1

    sorted_counts = counts.most_common()

    return int(sorted_counts[0][1] - sorted_counts[-1][1])


def generate_pair_matrix(polymer, rules):
    """
    Generate a state transition matrix from pair to pair
    E.g. 1 NN -> 1 NC + 1 CN
    E.g. 1 NB -> 1 NB (no insertion = no change)
    """
    # Turn rules into a dict
    rule_dict = {pair: inserted for pair, inserted in rules}

    # Generate list of all used elements
    rule_chars = "".join(["".join(r) for r in rules])
    all_chars = "".join([*list(polymer), *list(rule_chars)])
    chars = set(all_chars)

    # Generate all possible pairs
    pairs = list(itertools.product(chars, repeat=2))
    pairs = [''.join(pair) for pair in pairs]

    # Generate empty transition matrix
    mat = pd.DataFrame(index=pairs, columns=pairs).fillna(0)
    mat = mat.astype(np.uint64)

    # Fill transition matrix rows
    for pair in pairs:
        if pair not in rule_dict:
            mat.at[pair, pair] += 1
        
        else:
            inserted = rule_dict[pair]
            new_pairs = [pair[0] + inserted, inserted + pair[1]]

            for newp in new_pairs:
                mat.at[pair, newp] += 1

    return mat


def polymer_to_state(polymer: str):
    state = defaultdict(int)
    polymer = list(polymer)

    for tuplepair in zip(polymer, polymer[1:]):
        pair = "".join(tuplepair)
        state[pair] += 1

    return pd.Series(state)


if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')
