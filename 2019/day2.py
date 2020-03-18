program = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,9,19,1,10,19,23,2,9,23,27,1,6,27,31,2,31,9,35,1,5,35,39,1,10,39,43,1,10,43,47,2,13,47,51,1,10,51,55,2,55,10,59,1,9,59,63,2,6,63,67,1,5,67,71,1,71,5,75,1,5,75,79,2,79,13,83,1,83,5,87,2,6,87,91,1,5,91,95,1,95,9,99,1,99,6,103,1,103,13,107,1,107,5,111,2,111,13,115,1,115,6,119,1,6,119,123,2,123,13,127,1,10,127,131,1,131,2,135,1,135,5,0,99,2,14,0,0]
ex0 = [1,9,10,3,2,3,11,0,99,30,40,50]
ex1 = [1,0,0,0,99]
ex2 = [2,3,0,3,99]
ex3 = [2,4,4,5,99,0]
ex4 = [1,1,1,4,99,5,6,0,99]


def runIntCode(program):
    intCode = [i for i in program]
    pointer = 0
    instruction = intCode[pointer]


    while instruction != 99:
        paramA = intCode[pointer + 1]
        paramB = intCode[pointer + 2]
        paramC = intCode[pointer + 3]

        if instruction == 1:
            intCode[paramC] = intCode[paramA] + intCode[paramB]
        elif instruction == 2:
            intCode[paramC] = intCode[paramA] * intCode[paramB]
        else:
            print("Invalid instruction - Something went wrong!")
            print(instruction)
            break
        
        pointer += 4
        instruction = intCode[pointer]

    return intCode[0]


# Part one tests
assert runIntCode(ex0) == 3500
assert runIntCode(ex1) == 2
assert runIntCode(ex2) == 2
assert runIntCode(ex3) == 2
assert runIntCode(ex4) == 30


# Part one execution
modifiedProgram = [i for i in program]
modifiedProgram[1], modifiedProgram[2] = 12, 2
print(f'Part one: {runIntCode(modifiedProgram)}')


def findIntCodeInput(target):
    for noun in range(100):
        for verb in range(100):
            # workingMemory = copy.deepcopy(memory)
            workingMemory = [i for i in program]
            workingMemory[1] = noun
            workingMemory[2] = verb
            res = runIntCode(workingMemory)
            if (res == target):
                return 100 * noun + verb


# Part two execution
print(f'Part two: {findIntCodeInput(19690720)}')