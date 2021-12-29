from collections import Counter

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


def part_two():
    return diff_maxmin_freq_after_n_iterations(40)


if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')