def format_instruction(instruction:str):
    instruction = instruction.strip()
    if not instruction:
        return

    instruction = instruction.strip().split()
    target = instruction[-1]

    if instruction[0] == "NOT":
        op, a = instruction[0:2]
        return (target, (op, a))

    elif instruction[1] == "->":
        op, a = "->", instruction[0]
        return (target, (op, a))

    else:
        a, op, b = instruction[0:3]
        return (target, (op, a, b))


def is_known(param, signals):
    if param[0] in "0123456789":
        return int(param)
    elif param in signals:
        return signals[param]
    return -1


def part_one(instructions, target):
    signals = {}
    remaining_instructions = {k:v for k,v in instructions.items()}
    bitmask = int("0b1111_1111_1111_1111",2)

    # proceed until target signal value is found
    while target not in signals:
        processed = ""

        for key, val in remaining_instructions.items():
            op = val[0]
            a = is_known(val[1], signals)
            
            if len(val) == 2 and a >= 0:    
                if op == "->":
                    signals[key] = a

                elif op == "NOT":
                    signals[key] = ~a 
                
                signals[key] = signals[key] & bitmask
                # print(op, a, "->", signals[key], "@", key)
                processed = key
                break
            
            
            elif len(val) == 3:
                b = is_known(val[2], signals)
                if a >= 0 and b >= 0:
                    if op == "AND":
                        signals[key] = a & b

                    elif op == "OR":
                        signals[key] = a | b

                    elif op == "LSHIFT":
                        signals[key] = a << b

                    elif op == "RSHIFT":
                        signals[key] = a >> b
                    
                    signals[key] = signals[key] & bitmask
                    # print(op, a, b, "->", signals[key], "@", key)
                    processed = key
                    break

        if processed:
            # print(key, ", ", signals[key], ", ", isinstance(signals[key], int))
            remaining_instructions.pop(processed)
        else:
            print("\n\n\nNothing found to process! Remaining instructions:")
            for k,v in remaining_instructions.items():
                print(k,v)
            
            break
    else:
        print(signals.get("a"))
        return signals.get("a")


def part_two(instructions, target, override):
    instructions["b"] = ("->", str(override))
    part_one(instructions, target)



if __name__ == "__main__":
    with open("day7.txt") as file:
        puzzle_input = file.readlines()

    circuit = dict([format_instruction(instruction) for instruction in puzzle_input][0:-1])
    circuit = dict(circuit)

    a = part_one(circuit, "a")
    part_two(circuit, "a", a)