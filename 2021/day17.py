def read_input(raw = None):

    if not raw:
        with open('day17.txt') as f:
            raw = f.read().strip()

    raw = raw.lstrip("target area: ")
    x, _, y = raw.partition(", ")
    x = x[2:].partition("..")
    y = y[2:].partition("..")

    xmin, xmax = int(x[0]), int(x[2])
    ymin, ymax = int(y[0]), int(y[2])

    x = (xmin, xmax)
    y = (ymin, ymax)

    return x, y


# def hits_target_bf(vx, vy, target):
#     x, y = 0, 0

#     (xmin, xmax), (ymin, ymax) = target

#     while True:
#         x += vx
#         y += vy

#         if xmin <= x <= xmax and ymin <= y <= ymax:
#             return True

#         if x > xmax:
#             return False
        
#         if y < ymin and vy <= 0:
#             return False

#         vx -= 1
#         vy -= 1


def part_one(target = None):
    left, right, bottom, top = read_input(target)

    y = 0
    vy = 0
    
    vy_candidates = [v for v in range(bottom, -bottom -1)]


    


def sum_of_n_natural_nums(n):
    return v*(v+1)//2


def part_two():
    pass


if __name__ == '__main__':
    # print(f'Part one: {part_one()}')
    # print(f'Part two: {part_two()}')

    t = read_input('target area: x=20..30, y=-10..-5')
    # print(hits_target_bf(14,-4,t))

    part_one(t)