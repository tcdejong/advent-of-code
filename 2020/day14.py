def decode_address(address: int, float_str: str) -> list[int]:
    assert len(float_str) == 36
    num_floating = float_str.count("1")
    
    if num_floating == 0:
        return [address]

    working_copies = [address for _ in range(2**num_floating)]

    for i, address in enumerate(working_copies):
        x_mask = format(i, 'b').zfill(num_floating)
        x_mask_iter = iter(x_mask * 2)

        mask0 = [next(x_mask_iter) if c == "1" else "1" for c in float_str]
        mask1 = [next(x_mask_iter) if c == "1" else "0" for c in float_str]

        mask0 = int("".join(mask0), 2)
        mask1 = int("".join(mask1), 2)

        new_address = (address & mask0) | mask1
        working_copies[i] = new_address

    return working_copies


def part_one(program: list[str]) -> int:
    masks = (0, 0)
    memory = dict()

    for line in program:
        instruction, value = line.split(' = ')
        
        if instruction.startswith('mask'):
            masks = read_masks(value)
        
        else: 
            address = instruction[4:-1]
            masked_value = (int(value) & masks[0]) | masks[1]
            memory[address] = masked_value

    res = sum(memory.values())
    print(f'Part one: {res}')
    return res


def part_two(program: list[str], verbose = False) -> int:
    memory = dict()

    for line in program:
        # print(line)
        instruction, value = line.split(' = ')
        
        if instruction.startswith('mask'):
            mask_on = int(value.replace("X", "0"), 2)
            float_str = value.strip().replace("1", "0").replace("X","1")
        
        else: 
            masked_address = int(instruction[4:-1]) | mask_on
            for address in decode_address(masked_address, float_str):
                memory[address] = int(value)

    res = sum(memory.values())
    print(f'Part two: {res}')

    if verbose:
        h1, h2, h3 = "Key (Dec)", "Key (Binary)", "Value"
        print("Total entries:", len(memory))
        print(f"{h1:12}   :   {h2:36}   :   {h3}")

        for k,v in memory.items():
            b_str = format(k, 'b').zfill(36).replace('1', '#').replace('0', '.')
            print(f"{k:12}   :   {b_str}   :   {v}")

    return res


def read_input(file_path) -> list[str]:
    with open(file_path) as file:
        return file.readlines()


def read_masks(mask: str) -> tuple[int,int]:
    mask0 = mask.replace("X", "1")
    mask1 = mask.replace("X", "0")
    return (int(mask0,2), int(mask1,2))


if __name__ == '__main__':
    program = read_input('day14.txt')
    part_one(program)
    part_two(program)
