from typing import Literal, Tuple

TOperation = Tuple[str, str, str] | Tuple[str, str]
TInstr = Tuple[str, TOperation]

TInstrDict = dict[str, TOperation]

def format_instruction(instruction:str) -> TInstr:
    # Operand OP determines number of parameters and how they determine a signal value
    # Target is where the resulting signal value will be sent
    instruction = instruction.strip()
    if not instruction:
        return ('', ('NOOP', '', ''))

    instruction = instruction.strip().split()
    target = instruction[-1]

    if instruction[1] == "->":
        op, param1 = "->", instruction[0]
        return (target, (op, param1))

    if instruction[0] == "NOT":
        op, param1 = instruction[0:2]
        return (target, ('NOT', param1))

    else:
        param1, op, param2 = instruction[0:3]
        return (target, (op, param1, param2))


def is_known_signal_value(param, signals):
    if param[0] in "0123456789":
        return int(param)
    elif param in signals:
        return signals[param]
    return -1


def part_one(instructions: TInstrDict, output_signal: str):
    signals = {}
    remaining_instructions = {k:v for k,v in instructions.items()}
    bitmask = int("0b1111_1111_1111_1111",2)

    # proceed until target signal value is found
    while output_signal not in signals:
        processed = ""

        for key, val in remaining_instructions.items():
            op = val[0]
            a = is_known_signal_value(val[1], signals)
            
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
                b = is_known_signal_value(val[2], signals)
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
    with open("input.txt") as file:
        puzzle_input = file.readlines()

    instructions = [format_instruction(instruction) for instruction in puzzle_input][0:-1]
    circuit = dict(instructions)
    circuit = dict(circuit)

    a = part_one(circuit, "a")
    # part_two(circuit, "a", a)