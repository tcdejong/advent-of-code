import copy
import time

memory = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,10,19,23,2,9,23,27,1,6,27,31,2,31,9,35,1,5,35,39,1,10,39,43,1,10,43,47,2,13,47,51,1,10,51,55,2,55,10,59,1,9,59,63,2,6,63,67,1,5,67,71,1,71,5,75,1,5,75,79,2,79,13,83,1,83,5,87,2,6,87,91,1,5,91,95,1,95,9,99,1,99,6,103,1,103,13,107,1,107,5,111,2,111,13,115,1,115,6,119,1,6,119,123,2,123,13,127,1,10,127,131,1,131,2,135,1,135,5,0,99,2,14,0,0]

# ex0 = [1,9,10,3,2,3,11,0,99,30,40,50]
# ex1 = [1,0,0,0,99]
# ex2 = [2,3,0,3,99]
# ex3 = [2,4,4,5,99,0]
# ex4 = [1,1,1,4,99,5,6,0,99]


def runIntCode(intCode):
    pointer = 0
    instruction = intCode[pointer]


    while (True):
        paramA = intCode[pointer + 1]
        paramB = intCode[pointer + 2]
        paramC = intCode[pointer + 3]

        if instruction == 1:
            intCode[paramC] = intCode[paramA] + intCode[paramB]
            pointer += 4
        elif instruction == 2:
            intCode[paramC] = intCode[paramA] * intCode[paramB]
            pointer += 4
        elif instruction == 99:
            break
        else:
            print("Invalid instruction - Something went wrong!")
            print(instruction)
            break
        
        instruction = intCode[pointer]

        if instruction == 99:
            break

    return intCode

# memory[1] = 12
# memory[2] = 2
# print(runIntCode(memory))

# Intcode programs are given as a list of integers; these values are used as the initial state for the computer's memory. 
# When you run an Intcode program, make sure to start by initializing memory to the program's values. 
# A position in memory is called an address (for example, the first value in memory is at "address 0").

# Opcodes (like 1, 2, or 99) mark the beginning of an instruction. The values used immediately after an opcode, if any, are called the instruction's parameters. 
# For example, in the instruction 1,2,3,4, 1 is the opcode; 2, 3, and 4 are the parameters. The instruction 99 contains only an opcode and has no parameters.

# The address of the current instruction is called the instruction pointer; it starts at 0. 
# After an instruction finishes, the instruction pointer increases by the number of values in the instruction; 
# until you add more instructions to the computer, this is always 4 (1 opcode + 3 parameters) for the add and multiply instructions. 
# (The halt instruction would increase the instruction pointer by 1, but it halts the program instead.)

def findIntCodeInput(target):
    start = time.time()

    for noun in range(100):
        for verb in range(100):
            # workingMemory = copy.deepcopy(memory)
            workingMemory = copy.copy(memory)
            workingMemory[1] = noun
            workingMemory[2] = verb
            res = runIntCode(workingMemory)
            if (res[0] == target):
                print("Verb: ",verb," - Noun: ",noun, 100 * noun + verb, res[0])

    print(time.time() - start)


# findIntCodeInput(3760627)
findIntCodeInput(19690720)
