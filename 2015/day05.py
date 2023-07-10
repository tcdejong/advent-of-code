from itertools import zip_longest
from collections import defaultdict

# sliding window approach
def is_nice(word):
    letters = list(word)
    pairwise = zip_longest(letters, letters[1:])  

    naughty_strings = ["ab", "cd", "pq", "xy"]
    repeated_letter = False
    vowels = 0

    for a, b in pairwise:
        if b != None and "".join((a,b)) in naughty_strings:
            return False
        
        if a == b:
            repeated_letter = True

        if a in "aeoui":
            vowels += 1

    if vowels >= 3:
        return repeated_letter


assert is_nice("ugknbfddgicrmopn")
assert is_nice("aaa")
assert (not is_nice("jchzalrnumimnmhp"))
assert (not is_nice("haegwjzuvuyypxyu"))
assert (not is_nice("dvszwmarrgswjxmb"))


def is_really_nice(word):
    letters = list(word)
    itriplet = enumerate(zip_longest(letters, letters[1:], letters[2:]))  
    
    separated_repeat = False
    pairs = defaultdict(list)


    for i,(a,b,c) in itriplet:
        if a == c:
            separated_repeat = True

        pairs[(a,b)].append(i)

    if not separated_repeat:
        return False

    for val in pairs.values():
        if len(val) == 1:
            continue

        if val[-1] - val[0] >= 2:
            return True

    return False


assert is_really_nice("qjhvhtzxzqqjkmpb")
assert is_really_nice("xxyxx")
assert (not is_really_nice("uurcxstgmygtbstg"))
assert (not is_really_nice("ieodomkazucvgmuy"))


def part_one(puzzle_input):
    nice_strings = 0
    for word in puzzle_input:
        if is_nice(word):
            nice_strings += 1

    print(f"Pt1: {nice_strings} nice strings")


def part_two(puzzle_input):
    really_nice_strings = 0
    for word in puzzle_input:
        if is_really_nice(word):
            really_nice_strings += 1

    print(f"Pt2: {really_nice_strings} really nice strings")


if __name__ == "__main__":
    with open("day5.txt") as file:
        puzzle_input = file.readlines()

    part_one(puzzle_input)
    part_two(puzzle_input)