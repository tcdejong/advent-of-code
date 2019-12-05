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


nParams = {
    1: 3,
    2: 3,
    3: 1,
    4: 1,
    5: 2,
    6: 2,
    7: 3,
    8: 3,
    99: 0,
}

ADD = 1
MULT = 2
INP = 3
OUTP = 4
JIFT = 5
JIFF = 6
LT = 7
EQ = 8
HALT = 99

pointer = 0
instruction = -999

def runIntCode(intCode):
    global pointer
    global instruction

    while True:       
        instruction = intCode[pointer]
        opcode, modes = parseInstruction(intCode)
        params = intCode[pointer + 1 : pointer + 1 + nParams.get(opcode)]

        if opcode == ADD:
            a = params[0] if modes[0] == 1 else intCode[params[0]]
            b = params[1] if modes[1] == 1 else intCode[params[1]]
            intCode[params[2]] = a + b
            pointer += nParams.get(opcode) + 1
        elif opcode == MULT:
            a = params[0] if modes[0] == 1 else intCode[params[0]]
            b = params[1] if modes[1] == 1 else intCode[params[1]]
            intCode[params[2]] = a * b
            pointer += nParams.get(opcode) + 1
        elif opcode == INP:
            # id = input("Enter T.E.S.T. system ID:")
            id = 5
            a = params[0]
            intCode[a] = int(id)
            pointer += nParams.get(opcode) + 1
        elif opcode == OUTP:
            a = params[0] if modes[0] == 1 else intCode[params[0]]
            print("Diagnostic output:", a, sep=" ")
            pointer += nParams.get(opcode) + 1
        elif opcode == JIFT:
            a = params[0] if modes[0] == 1 else intCode[params[0]]
            b = params[1] if modes[1] == 1 else intCode[params[1]]
            pointer = b if a != 0 else pointer + nParams.get(opcode) + 1
        elif opcode == JIFF:
            a = params[0] if modes[0] == 1 else intCode[params[0]]
            b = params[1] if modes[1] == 1 else intCode[params[1]]
            pointer = b if a == 0 else pointer + nParams.get(opcode) + 1
        elif opcode == LT:
            a = params[0] if modes[0] == 1 else intCode[params[0]]
            b = params[1] if modes[1] == 1 else intCode[params[1]]
            intCode[params[2]] = 1 if a < b else 0
            pointer += nParams.get(opcode) + 1
        elif opcode == EQ:
            a = params[0] if modes[0] == 1 else intCode[params[0]]
            b = params[1] if modes[1] == 1 else intCode[params[1]]
            intCode[params[2]] = 1 if a == b else 0
            pointer += nParams.get(opcode) + 1
        elif opcode == HALT:
            break
        else:
            print("Invalid instruction - Something went wrong!")
            print(intCode[pointer], opcode)
            break

    return intCode


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

    return (opcode, modes)


intCode = [3,225,1,225,6,6,1100,1,238,225,104,0,1001,210,88,224,101,-143,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,101,42,92,224,101,-78,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1101,73,10,225,1102,38,21,225,1102,62,32,225,1,218,61,224,1001,224,-132,224,4,224,102,8,223,223,1001,224,5,224,1,224,223,223,1102,19,36,225,102,79,65,224,101,-4898,224,224,4,224,102,8,223,223,101,4,224,224,1,224,223,223,1101,66,56,224,1001,224,-122,224,4,224,102,8,223,223,1001,224,2,224,1,224,223,223,1002,58,82,224,101,-820,224,224,4,224,1002,223,8,223,101,3,224,224,1,223,224,223,2,206,214,224,1001,224,-648,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,76,56,224,1001,224,-4256,224,4,224,102,8,223,223,1001,224,6,224,1,223,224,223,1102,37,8,225,1101,82,55,225,1102,76,81,225,1101,10,94,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,8,226,677,224,102,2,223,223,1005,224,329,101,1,223,223,1008,677,677,224,1002,223,2,223,1006,224,344,1001,223,1,223,107,226,677,224,102,2,223,223,1005,224,359,1001,223,1,223,1108,677,677,224,1002,223,2,223,1006,224,374,101,1,223,223,1107,677,677,224,1002,223,2,223,1006,224,389,101,1,223,223,108,226,677,224,102,2,223,223,1006,224,404,101,1,223,223,7,677,677,224,102,2,223,223,1006,224,419,101,1,223,223,108,677,677,224,102,2,223,223,1006,224,434,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,449,1001,223,1,223,108,226,226,224,102,2,223,223,1005,224,464,101,1,223,223,8,226,226,224,1002,223,2,223,1006,224,479,101,1,223,223,1008,226,226,224,102,2,223,223,1005,224,494,1001,223,1,223,1008,677,226,224,1002,223,2,223,1005,224,509,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,524,101,1,223,223,1007,677,226,224,1002,223,2,223,1006,224,539,1001,223,1,223,1108,677,226,224,102,2,223,223,1005,224,554,1001,223,1,223,8,677,226,224,1002,223,2,223,1005,224,569,101,1,223,223,1108,226,677,224,1002,223,2,223,1005,224,584,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,599,101,1,223,223,107,226,226,224,102,2,223,223,1006,224,614,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,629,1001,223,1,223,1107,226,677,224,1002,223,2,223,1006,224,644,101,1,223,223,1007,677,677,224,102,2,223,223,1006,224,659,1001,223,1,223,1007,226,226,224,1002,223,2,223,1006,224,674,1001,223,1,223,4,223,99,226]

runIntCode(intCode)