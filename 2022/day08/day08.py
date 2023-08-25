def read_input(filename: str = 'day08.txt'):
    with open(filename) as f:
        data = [line.strip() for line in f.readlines()]

    return data


def part_one(trees):
    visible_trees = set()

    x_max = len(trees[0])
    y_max = len(trees)

    # raycast from top
    for x in range(x_max):
        current_tallest = -1
        for y in range(y_max):
            height = int(trees[y][x])
            if height > current_tallest:
                visible_trees.add((x,y))
                current_tallest = height
            
            if current_tallest == 9:
                break

    # raycast from bottom
    for x in range(x_max):
        current_tallest = -1
        for y in range(y_max-1,-1,-1):
            height = int(trees[y][x])
            if height > current_tallest:
                visible_trees.add((x,y))
                current_tallest = height
            
            if current_tallest == 9:
                break
    
    # raycast from left
    for y in range(y_max):
        current_tallest = -1
        for x in range(x_max):
            height = int(trees[y][x])
            if height > current_tallest:
                visible_trees.add((x,y))
                current_tallest = height
            
            if current_tallest == 9:
                break

    # raycast from right
    for y in range(y_max):
        current_tallest = -1
        for x in range(x_max-1, -1, -1):
            height = int(trees[y][x])
            if height > current_tallest:
                visible_trees.add((x,y))
                current_tallest = height
            
            if current_tallest == 9:
                break

    return len(visible_trees)         


def part_two(trees):
    top_score = 0
    
    x_max = len(trees[0])
    y_max = len(trees)

    # slide a pointer over 1 row or column of trees
    # keep 10 counters for visibility opposite to the direction of travel, 1 counter for each possible height
        # when observing tree (x,y) with height h, determine its visibility the counter for h
        # reset the height of all counters h and smaller (because on the next step, the tree blocks them but a bigger tree can look over them again)
        # increment all counters by 1
        # observe next tree

    scores = {(x,y):1 for x in range(x_max) for y in range(y_max)}

    # left->right
    for y in range(y_max):
        viewing_distance = [0 for _ in range(10)]
        for x in range(x_max):
            tree_pos = (x,y)

            tree_height = int(trees[y][x])
            scores[tree_pos] = scores[tree_pos] * viewing_distance[tree_height]

            viewing_distance[0:tree_height+1] = [0 for _ in range(tree_height+1)]
            viewing_distance = [x+1 for x in viewing_distance]

            assert len(viewing_distance) == 10


    # right->left
    for y in range(y_max):
        viewing_distance = [0 for _ in range(10)]
        for x in range(x_max-1,-1,-1):
            tree_pos = (x,y)

            tree_height = int(trees[y][x])
            scores[tree_pos] = scores[tree_pos] * viewing_distance[tree_height]

            viewing_distance[0:tree_height+1] = [0 for _ in range(tree_height+1)]
            viewing_distance = [x+1 for x in viewing_distance]

            assert len(viewing_distance) == 10
    
    # top->down
    for x in range(x_max):
        viewing_distance = [0 for _ in range(10)]
        for y in range(y_max):
            tree_pos = (x,y)

            tree_height = int(trees[y][x])
            scores[tree_pos] = scores[tree_pos] * viewing_distance[tree_height]

            viewing_distance[0:tree_height+1] = [0 for _ in range(tree_height+1)]
            viewing_distance = [x+1 for x in viewing_distance]

            assert len(viewing_distance) == 10

    # bottom->up
    for x in range(x_max):
        viewing_distance = [0 for _ in range(10)]
        for y in range(y_max-1,-1,-1):
            tree_pos = (x,y)

            tree_height = int(trees[y][x])
            scores[tree_pos] = scores[tree_pos] * viewing_distance[tree_height]

            viewing_distance[0:tree_height+1] = [0 for _ in range(tree_height+1)]
            viewing_distance = [x+1 for x in viewing_distance]

            assert len(viewing_distance) == 10


    return max(scores.values())


if __name__ == '__main__':
    puzzle_input = read_input()
    # print(f'Part one: {part_one(puzzle_input)}')
    print(f'Part two: {part_two(puzzle_input)}')