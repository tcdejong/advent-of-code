from collections import defaultdict

def read_input(file_path='day10.txt'):
    with open(file_path) as file:
        return [int(i) for i in file.readlines()]


def part_one():
    adapters = read_input()
    adapters.sort()   
    jolts = [0, *adapters, adapters[-1]+3]

    differences = defaultdict(int)
    for i,j in zip(jolts[1:], jolts):
        differences[i-j] += 1

    print(differences[1] * differences[3])
    

def part_two():
    adapters = read_input('day10ante.txt')
    adapters.sort()

    jolts = [0, *adapters, adapters[-1] + 3]

    num_paths = [0 for _ in jolts]
    num_paths[0] = 1

    for i, jolt in enumerate(jolts):
        for j in range(1,4):
            if i+j >= len(jolts):
                continue 

            diff = jolts[i+j] - jolt
            if diff <= 3:
                num_paths[i+j] += num_paths[i]

    return num_paths[-1]


if __name__ == '__main__':
    # part_one()
    res = part_two()
    print('found result, truncating...')

    res = str(res)

    

    i = -1
    while res[i] == "0":
        i -= 1

    res = res[:i+1]

    print(res[-10:])



