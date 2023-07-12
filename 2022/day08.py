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
    
        

            


def part_two(puzzle_input):
    pass


if __name__ == '__main__':
    puzzle_input = read_input()
    print(f'Part one: {part_one(puzzle_input)}')
    # print(f'Part two: {part_two(puzzle_input)}')