##### Documentation
# Opcode 1:  add two params 1 and 2 and store in position 3
# Opcode 2:  multiply two params 1 and 2 and store in position 3
# opcode 3:  take single integer as input
# opcode 4:  output single integer
# Opcode 99: Halt program

# params have two modes:
# 0: position, use the value stored at the position from this parameter
# 1: immediate, use the value directly

# opcodes and param modes are stored in a single integer. 
# The rightmost two digits are for the opcode
# the other digits, right to left, are the modes for params
# leading zeros are trimmed, but still count conceptually.
# ABCDE
#  1002 
# opcode 02 = 2, 
# C = 1st param mode, B 2nd param mode, A 3rd param (leading 0)

import os
import sys

pointer = 0
its = 0

nParams = {
        1: 3,
        2: 3,
        3: 1,
        4: 1,
        99: 0,
    }

def runIntCode(intCode):
    global pointer
    global its
    while True:        
        opcode, params = parseInstruction(intCode)
        its += 1

        if opcode == 1:
            intCode[params[2]] = params[0] + params[1]
        elif opcode == 2:
            intCode[params[2]] = params[0] + params[1]
        elif opcode == 3:
            # id = input("TEST component ID:")
            id = 1
            intCode[params[0]] = int(id)
        elif opcode == 4:
            print(params[0])
        elif opcode == 99:
            break
        else:
            print("Invalid instruction - Something went wrong!")
            print(intCode[pointer], opcode)
            break

        pointer += nParams.get(opcode) + 1

    return intCode


def parseInstruction(intCode):
    instruction = intCode[pointer]
    digits = list(map(int, list(str(instruction)))) # Ew
    modes = []
    params = []

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
    willOutput = (opcode in [1, 2, 4])

    for i in range(len(modes)):
        mode = modes[i]
        if i == len(modes) - 1 and willOutput:
            params.append(pointer + i + 1)
        elif mode == 0:
            pos = intCode[pointer + i + 1]
            params.append(intCode[pos])
        elif mode == 1:
            params.append(intCode[pointer + i + 1])
        else:
            print("Invalid parameter mode - Something went wrong!")
            print(intCode[instruction], mode)
    
    return (opcode, params)


intCode = [3,225,1,225,6,6,1100,1,238,225,104,0,1001,210,88,224,101,-143,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,101,42,92,224,101,-78,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1101,73,10,225,1102,38,21,225,1102,62,32,225,1,218,61,224,1001,224,-132,224,4,224,102,8,223,223,1001,224,5,224,1,224,223,223,1102,19,36,225,102,79,65,224,101,-4898,224,224,4,224,102,8,223,223,101,4,224,224,1,224,223,223,1101,66,56,224,1001,224,-122,224,4,224,102,8,223,223,1001,224,2,224,1,224,223,223,1002,58,82,224,101,-820,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,2,206,214,224,1001,224,-648,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,76,56,224,1001,224,-4256,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,1102,37,8,225,1101,82,55,225,1102,76,81,225,1101,10,94,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,8,226,677,224,102,2,223,223,1005,224,329,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,344,1001,223,1,223,107,226,677,224,102,2,223,223,1005,224,359,1001,223,1,223,1108,677,677,224,1002,223,2,223,1006,224,374,101,1,223,223,1107,677,677,224,1002,223,2,223,1006,224,389,101,1,223,223,108,226,677,224,102,2,223,223,1006,224,404,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,419,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,434,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,449,1001,223,1,223,108,226,226,224,102,2,223,223,1005,224,464,101,1,223,223,8,226,226,224,1002,223,2,223,1006,224,479,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,494,1001,223,1,223,1008,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,524,101,1,223,223,1007,677,226,224,1002,223,2,223,1006,224,539,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,554,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,569,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,599,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,614,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,629,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,659,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]

print(runIntCode(intCode))