##### Documentation
# Program: sequence of intcode instructions and parameters
# Instruction: opcode and modes for parameters
#   Rightmost two digits of the instruction are the opcode
#   Other digits are modes for parameters, right to left
#   Leading zeros are trimmed, but count as positional indicators
# Modes:
#   0: position, use the value stored at the position stored at this position
#   1: immediate, use the value stored at this position
# Operation: one instruction plus its parameters

# The rightmost two digits are for the opcode
# the other digits, right to left, are the modes for params
# leading zeros are trimmed, but still count conceptually.

# Opcodes:
# 1:  ADD:   add two params 1 and 2 and store in position 3
# 2:  MULT:  multiply two params 1 and 2 and store in position 3
# 3:  INP:   take single external input and save it to pos of param 1
# 4:  OUTP:  outputs whatever is in the position of param 1
# 5:  JIFT:  If param 1 is non-zero, set the pointer to the value from param 2
# 6:  JIFF:  If param 1 is zero, set the pointer to the value from param 2
# 7:  LT:    If param 1 is less than param 2, store 1 in the position given by param 3. Else store 0.
# 8:  EQ:    If param 1 is equal to param 2, store 1 in the position given by param 3. Else store 0.
# 99: HALT:  Halt program

# Example instruction:
# ABCDE (labels)
#  1002 (digits)
# DE = opcode = 02 = 2 = MULT, 
# C = 1st param mode, 
# B = 2nd param mode, 
# A 3rd param (leading 0)


ADD = 1
MULT = 2
INP = 3
OUTP = 4
JIFT = 5
JIFF = 6
LT = 7
EQ = 8
HALT = 99

nParams = {
    ADD: 3,
    MULT: 3,
    INP: 1,
    OUTP: 1,
    JIFT: 2,
    JIFF: 2,
    LT: 3,
    EQ: 3,
    HALT: 0,
}

pointer = 0
instruction = -999


def runIntCode(intCode):
    global pointer
    global instruction

    while True:       
        instruction = intCode[pointer]
        opcode, par = parseInstruction(intCode)

        if opcode == ADD:
            intCode[par[2]] = intCode[par[0]] + intCode[par[1]]
        elif opcode == MULT:
            intCode[par[2]] = intCode[par[0]] * intCode[par[1]]
        elif opcode == INP:
            inp = int(input("Input required:"))
            intCode[par[0]] = inp
        elif opcode == OUTP:
            print("Program output:" + str(intCode[par[0]]))
        elif opcode == JIFT:
            if intCode[par[0]] != 0: 
                pointer = intCode[par[1]]
                continue
        elif opcode == JIFF:
            if intCode[par[0]] == 0:
                pointer = intCode[par[1]]
                continue
        elif opcode == LT:
            intCode[par[2]] = 1 if intCode[par[0]] < intCode[par[1]] else 0
        elif opcode == EQ:
            intCode[par[2]] = 1 if intCode[par[0]] == intCode[par[1]] else 0
        elif opcode == HALT:
            break
        else:
            print("Invalid instruction - Something went wrong!")
            print(intCode[pointer], opcode)
            break

        pointer += nParams.get(opcode) + 1

    print("Program execution completed.")


def parseInstruction(intCode):
    digits = list(map(int, list(str(instruction)))) # Ew
    modes = []

    if len(digits) <= 2:
        opcode = instruction
    elif digits[-2] == 0: 
        opcode = digits[-1]
        modes = digits[0:-2]
    elif digits[-2] == 9 and digits[-1] == 9:
        opcode = 99

    leadingZeros = nParams.get(opcode) - len(modes)
    modes = leadingZeros * [0] + modes
    modes.reverse()

    params = list(range(pointer + 1, pointer + 1 + nParams.get(opcode)))
    for i in range(nParams.get(opcode)):
        if modes[i] == 0:
            params[i] = intCode[params[i]]

    return (opcode, params)


programs = {
    "ex1": [3,0,4,0,99],
    "ex2": [1002,4,3,4,33],
    "ex3": [3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9],
    "ex4": [3,3,1105,-1,9,1101,0,0,12,4,12,99,1],
    "ex5": [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99],
    "diag": [3,225,1,225,6,6,1100,1,238,225,104,0,1001,210,88,224,101,-143,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,101,42,92,224,101,-78,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1101,73,10,225,1102,38,21,225,1102,62,32,225,1,218,61,224,1001,224,-132,224,4,224,102,8,223,223,1001,224,5,224,1,224,223,223,1102,19,36,225,102,79,65,224,101,-4898,224,224,4,224,102,8,223,223,101,4,224,224,1,224,223,223,1101,66,56,224,1001,224,-122,224,4,224,102,8,223,223,1001,224,2,224,1,224,223,223,1002,58,82,224,101,-820,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,2,206,214,224,1001,224,-648,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,76,56,224,1001,224,-4256,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,1102,37,8,225,1101,82,55,225,1102,76,81,225,1101,10,94,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,8,226,677,224,102,2,223,223,1005,224,329,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,344,1001,223,1,223,107,226,677,224,102,2,223,223,1005,224,359,1001,223,1,223,1108,677,677,224,1002,223,2,223,1006,224,374,101,1,223,223,1107,677,677,224,1002,223,2,223,1006,224,389,101,1,223,223,108,226,677,224,102,2,223,223,1006,224,404,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,419,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,434,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,449,1001,223,1,223,108,226,226,224,102,2,223,223,1005,224,464,101,1,223,223,8,226,226,224,1002,223,2,223,1006,224,479,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,494,1001,223,1,223,1008,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,524,101,1,223,223,1007,677,226,224,1002,223,2,223,1006,224,539,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,554,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,569,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,599,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,614,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,629,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,659,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]
}


def listPrograms(error=False):
    message = "Program not found! Valid program names are:" if error else "Choose a program:"
    
    print("-" * 20)
    print(message)
    for key in programs.keys():
        print("-- " + key)
    print("-" * 20)


def run():
    listPrograms()
    while True:
        programName = input("Program name:")
        if programName in programs:
            program = programs.get(programName)
            break
        else:
            listPrograms(True)
    runIntCode(program)

run()