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

import itertools

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

instruction = -999


def runIntCode(intCode, inputs):
    pointer = 0
    global instruction
    out = -999
    while True:       
        instruction = intCode[pointer]
        opcode, par = parseInstruction(intCode, pointer)

        if opcode == ADD:
            intCode[par[2]] = intCode[par[0]] + intCode[par[1]]
        elif opcode == MULT:
            intCode[par[2]] = intCode[par[0]] * intCode[par[1]]
        elif opcode == INP:
            inp = inputs.pop(0)
            intCode[par[0]] = inp
        elif opcode == OUTP:
            out = intCode[par[0]]
            # print("Program output:" + str(intCode[par[0]]))
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

    return out


def parseInstruction(intCode, pointer):
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
    "ex1": [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],
    "ex2": [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0],
    "ex3": [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0],
    "boosters": [3,8,1001,8,10,8,105,1,0,0,21,38,63,72,85,110,191,272,353,434,99999,3,9,102,4,9,9,101,2,9,9,102,3,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,1001,9,5,9,1002,9,5,9,101,3,9,9,4,9,99,3,9,1001,9,2,9,4,9,99,3,9,1001,9,3,9,102,2,9,9,4,9,99,3,9,101,2,9,9,102,2,9,9,1001,9,2,9,1002,9,4,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99]
}


def listPrograms(error=False):
    message = "Program not found! Valid program names are:" if error else "Choose a program:"
    
    print("-" * 20)
    print(message)
    for key in programs.keys():
        print("-- " + key)
    print("-" * 20)


def run():
    phaseCodes = itertools.permutations(range(0, 5))
    maxThrusters = 0

    for order in phaseCodes:
        thrust = runPhaseCodeSequence(order)
        if thrust > maxThrusters:
            maxThrusters = thrust

    print(maxThrusters)

def runPhaseCodeSequence(seq):
    res = 0
    for val in seq:
        program = programs["boosters"]
        inputs = [val, res]
        res = runIntCode(program, inputs)
    return res

run()