def read_input(fp='day19.txt') -> tuple[dict, list]:
    """
    Read and format puzzle input
    Return dictionary of rules and list of messages
    """

    with open(fp) as file:
        lines = file.readlines()

    rules = [line.strip().partition(':') for line in lines if line[0].isnumeric()]
    messages = [line.strip() for line in lines if line[0].isalpha()]

    rules_dict = {int(key): clean_rule(val) for (key, _, val) in rules}

    return rules_dict, messages


def clean_rule(rule:str):
    """
    Clean a rule-string that could be any of these three cases:
        1. a rule to match a single character, e.g. >"a"<
        2. a rule to match n characters to n other rules, e.g. >13 34< for n=2
        3. a rule to match n characters to either of two rules of type 2., 
    """

    def clean_segment(segment):
        "Convert a rule of type 1 or 2 from str to a str or tuple of ints"
        print(f'cleaning {segment=}')

        # Case: rule is type 1
        if '"' in rule:
            return rule[-2]

        # Case: rule is type 2
        vals = tuple(int(x) for x in segment.split())
        return vals


    if '|' in rule:
        # Case: rule is type 3 
        l, _, r = rule.partition('|')
        return (clean_segment(l), clean_segment(r))
    else:
        # Case: rule is type 1, 2
        return clean_segment(rule)



def resolve_rules(rules):
    """ Convert rules referring to other rules to rules of valid (matching) substrings"""
    resolved = {} # dict mapping a full rule,   e.g. 2, 3 | 4, 5, to matching substrings
    partials = {} # dict mapping a single rule, e.g. 2,           to matching substrings


    def resolve_single(rule_num, rules, resolved, partials):
        """SIDE EFFECTS! Modifies resolved and partials in place"""

        r = rules[rule_num]

        if isinstance(r, str):
            resolved[rule_num] = r
            return
        
        if isinstance(r[0], int):
            # r is shape (1,2,3,..,n)
            pass

        if isinstance(r[0], tuple):
            pass
            # resolve_single()



    for rule_num in rules:
        if rule_num not in resolved:
            resolve_single(rule_num, rules, resolved, partials)


    return resolved
        
            



def test_message(message, rules):
    pass


rules, messages = read_input("day19ex.txt")
[print(rule) for rule in rules.values()]

resolved = resolve_rules(rules)

for message in messages:
    test_message(message, rules)