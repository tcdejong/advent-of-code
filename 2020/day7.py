# bags must be color coded
# and contain specifric quantities of other color-coded bags

import networkx as nx
from networkx.classes.digraph import DiGraph

def bags_inside(color, rules):
    contained_bags = rules[color]

    bags = 0

    for inner_color, properties in contained_bags.items():
        inner_count = properties['weight']
        bags += inner_count * (1 + bags_inside(inner_color, rules))

    return bags


def read_input(file_path = 'day7.txt'):
    with open(file_path) as file:
        return file.readlines()


def parse_rules(data):
    rules = nx.DiGraph()

    # This could be regex, but it gets messy
    for line in data:
        line = line.strip()[:-5]
        line = line.replace('bags', 'bag')
        outer, _, inner = line.partition(" contain ")
        outer = outer[:-4]
        inner = inner.strip()

        if outer not in rules:
            rules.add_node(outer)

        if inner == "no other":
            continue

        inner = inner.split(' bag, ')

        for option in inner:
            count, _, inner_color = option.partition(" ")
            count = int(count)

            if inner_color not in rules:
                rules.add_node(inner_color)
            
            rules.add_edge(outer, inner_color, weight=count)

    return rules


def part_one(rules:DiGraph):
    outer_colors = set()
    search = set(['shiny gold'])
    seen = set()

    while search:
        target = search.pop()
        seen.add(target)
        predecessors = [color for color in rules.predecessors(target) if color not in seen]
        [(search.add(color), outer_colors.add(color)) for color in predecessors]

    print(len(outer_colors))


def part_two(rules:DiGraph):
    print(bags_inside('shiny gold',rules))


if __name__ == '__main__':
    data = read_input()
    rules = parse_rules(data)

    part_one(rules)
    part_two(rules)
