from typing import Counter


L_CHARS = "([{<"
R_CHARS = ")]}>"
L_FROM_R = {k:v for k, v in zip(R_CHARS, L_CHARS)}
R_FROM_L = {k:v for k, v in zip(L_CHARS, R_CHARS)}

SCORES_P1 = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

SCORES_P2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}



def read_input(filename: str = 'day10.txt'):
    with open(filename) as f:
        lines = (line.strip() for line in f)
        lines = [line for line in lines if line]

    return lines


def corruption_score(line:str, part=1):
    """
    a corrupted line is one where a chunk closes with the wrong character
    Examples of corrupted chunks include (], {()()()>, (((()))}, and <([]){()}[{}])
    A score of 0 means the line is not corrupted
    """
    
    open_stack = ""
    
    for c in line:
        if c in L_CHARS:
            open_stack += c
        else:
            if open_stack[-1] == L_FROM_R[c]:
                open_stack = open_stack[:-1]
            else:
                return SCORES_P1[c] if part == 1 else 0
            
    if part == 1:
        return 0

    closing_chars = [R_FROM_L[c] for c in open_stack[::-1]]
    score = 0

    for c in closing_chars:
        score = score * 5 + SCORES_P2[c]

    return score


def part_one():
    data = read_input("day10.txt")
    return sum(corruption_score(line) for line in data)


def part_two():
    data = read_input("day10.txt")
    scores = [corruption_score(line, part=2) for line in data]
    scores = [s for s in scores if s != 0]

    scores = sorted(scores)
    print(scores)

    winner = int((len(scores)-1)/2)
    return scores[winner]


if __name__ == '__main__':
    print(f'Part one: {part_one()}')
    print(f'Part two: {part_two()}')

    assert corruption_score("(]") > 0
    assert corruption_score("{()()()>,") > 0
    assert corruption_score("(((()))}") > 0
    assert corruption_score("<([]){()}[{}])") > 0