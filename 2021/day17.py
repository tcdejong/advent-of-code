from collections import defaultdict

def read_input():
    with open('day17.txt') as f:
        raw = f.read().strip()

    raw = raw.lstrip("target area: ")
    x, _, y = raw.partition(", ")
    x = x[2:].partition("..")
    y = y[2:].partition("..")

    left, right = int(x[0]), int(x[2])
    bottom, top = int(y[0]), int(y[2])

    return left, right, bottom, top


def part_one(target):
    left, right, bottom, top = target

    vy = 0
    
    # If target below 0: use symmetry of trajectory: 
    # falling projectile is back at y=0 after a few ticks
    # to not overshoot, vy = speed to the bottom
    # eg bottom of target is at y=-5, then vy=-5 when crossing, so it was shot up at 4:
    # t       vy      y
    # 0       4       0     shot
    # 1       3       4
    # 2       2       7
    # 3       1       9
    # 4       0       10    apex
    # 5       -1      10    apex
    # 6       -2      9
    # 7       -3      7
    # 8       -4      4
    # 9       -5      0     crossing y=0
    # 10      -6      -5    target

    # OFF BY 1! We shoot up with 1 less vy than the bottom of the target is located

    # if target is above 0:
    # shoot top top immediately
    # vy = top

    assert top != 0 # if top is 0 we can shoot up to infinity 

    if top > 0:
        vy = top
    else:
        vy = abs(bottom) -1 


    # Because target area is square, both dimensions are independent
    # x does not matter

    return sum_of_n_natural_nums(vy)


def part_two(target):
    # for vx and vy, independently decide at which ticks they hit.
    # Then combine results
    # Account for x=0 dropping vertically -> missing X values

    left, right, bottom, top = target
    print(target)

    # assume target always negative
    assert top < 0

    min_vy = bottom
    max_vy = abs(bottom) + 1
    max_vx = right
    max_t = 2 * max_vy + 1

    
    
    hits_at_tick = {} # structure: hits_at_tick[t][vx: list, vy:list]



    # determine min vx by brute force
    min_vx = left
    while True:
        if sum_of_n_natural_nums(min_vx) >= left:
            min_vx -= 1
        else:
            min_vx += 1
            break

    print(f'{min_vx=}, {max_vx=}, {min_vy=}, {max_vy=}, {max_t=}')
    
    # test hits for each vx between determined min and max
    for _vx in range(min_vx, max_vx + 1):
        t = 0
        vx = _vx
        x = 0
        while t <= max_t and x <= right:
            x += vx
            vx -= 1
            t += 1

            if left <= x <= right:
                if t not in hits_at_tick:
                    hits_at_tick[t] = defaultdict(set)
                
                hits_at_tick[t]['x'].add(_vx)
            
            elif x > right: # end the while, not the for
                vx = -1


    # test hits for each vy between determined min and max
    for _vy in range(min_vy, max_vy + 1):
        t = 0
        vy = _vy
        y = 0
        while y >= bottom:
            y += vy
            vy -= 1
            t += 1

            if bottom <= y <= top:
                if t not in hits_at_tick:
                    hits_at_tick[t] = defaultdict(set)
                
                hits_at_tick[t]['y'].add(_vy)

    options_per_tick = [len(t['x']) * len(t['y']) for t in hits_at_tick.values()]

    # for each vy option,
    # add options where vx = 0, so it is missing from t['x']
    for t, d in hits_at_tick.items():
        # t is an int for the tick number
        # d contains keys x and y for the initial velocity options found so far
        vys = d['y']


    print(sum(options_per_tick))

    options = [(vx, vy) for t in hits_at_tick.values() for vx in t['x'] for vy in t['y']]

    compare_to_example(options)

    return options


def compare_to_example(options: list[tuple[int, int]]):
    ex_raw = """23,-10  25,-9   27,-5   29,-6   22,-6   21,-7   9,0     27,-7   24,-5
25,-7   26,-6   25,-5   6,8     11,-2   20,-5   29,-10  6,3     28,-7
8,0     30,-6   29,-8   20,-10  6,7     6,4     6,1     14,-4   21,-6
26,-10  7,-1    7,7     8,-1    21,-9   6,2     20,-7   30,-10  14,-3
20,-8   13,-2   7,3     28,-8   29,-9   15,-3   22,-5   26,-8   25,-8
25,-6   15,-4   9,-2    15,-2   12,-2   28,-9   12,-3   24,-6   23,-7
25,-10  7,8     11,-3   26,-7   7,1     23,-9   6,0     22,-10  27,-6
8,1     22,-8   13,-4   7,6     28,-6   11,-4   12,-4   26,-9   7,4
24,-10  23,-8   30,-8   7,0     9,-1    10,-1   26,-5   22,-9   6,5
7,5     23,-6   28,-10  10,-2   11,-1   20,-9   14,-2   29,-7   13,-3
23,-5   24,-8   27,-9   30,-7   28,-5   21,-10  7,9     6,6     21,-5
27,-10  7,2     30,-9   21,-8   22,-7   24,-9   20,-6   6,9     29,-5
8,-2    27,-8   30,-5   24,-7"""

    ex_options = [tuple(int(i) 
    for i in item.split(',')) 
    for line in ex_raw.splitlines() 
    for item in line.split()]

    ex_options = set(ex_options)
    options = set(options)

    wrong_options = options - ex_options
    missing_options = ex_options - options

    if wrong_options:
        print("Options that are falsely included:")
        print(wrong_options)

    if missing_options:
        print("Options missing:")
        print(missing_options)




def sum_of_n_natural_nums(n):
    return n*(n+1)//2



def brute_force(vx, vy, target):
    x = 0
    y = 0
    t = 0
    left, right, bottom, top = target
    xmax = right
    ymin = bottom

    while x <= xmax and y >= ymin:
        msg = f'{t=}: ({x},{y})'
        if left <= x <= right and bottom <= y <= top:
            msg += ' - Hit!'
        print(msg)

        t += 1
        x += vx
        y += vy
        vx = max(vx-1, 0)
        vy -= 1
    else:
        print('next step would be:')
        msg = f'{t=}: ({x},{y})'
        if left <= x <= right and bottom <= y <= top:
            msg += ' - Hit!'
        print(msg)




if __name__ == '__main__':
    full_target = read_input()
    ex_target = 20, 30, -10, -5

    
    target = ex_target

    # print(f'Part one: {part_one(target)}')
    # print(f'Part two: {part_two(target)}')

    res = part_two(target)
    # 1916 too low
