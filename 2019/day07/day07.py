from copy import deepcopy
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

class intCodeComputer:
    def __init__(self, program, pointer=0):
        self.program = deepcopy(program)
        self.pointer = deepcopy(pointer)
        self.inp = []
        self.out = []


    def test(self):
        return self.pointer

    def runIntCode(self, inputs):
        intCode = self.program
        pointer = self.pointer

        # inputs = cleanInputs(inputs)
        while True:       
            opcode, par = self.parseInstruction()

            if opcode == ADD:
                intCode[par[2]] = intCode[par[0]] + intCode[par[1]]
            elif opcode == MULT:
                intCode[par[2]] = intCode[par[0]] * intCode[par[1]]
            elif opcode == INP:
                if len(inputs) == 0:
                    break
                intCode[par[0]] = inputs.pop(0)
            elif opcode == OUTP:
                self.out = intCode[par[0]]
                self.pointer += nParams[opcode] + 1
                break
                # print("Program output:" + str(intCode[par[0]]))
            elif opcode == JIFT:
                if intCode[par[0]] != 0: 
                    self.pointer = intCode[par[1]]
                    continue
            elif opcode == JIFF:
                if intCode[par[0]] == 0:
                    self.pointer = intCode[par[1]]
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

            self.pointer += nParams[opcode] + 1

        return self.out

        


    def parseInstruction(self):
        intCode = self.program
        pointer = self.pointer
        instruction = intCode[pointer]
        digits = list(map(int, list(str(instruction)))) # Ew
        modes = []

        if len(digits) <= 2:
            opcode = instruction
        elif digits[-2] == 0: 
            opcode = digits[-1]
            modes = digits[0:-2]
        elif digits[-2] == 9 and digits[-1] == 9:
            opcode = 99
        else:
            raise RuntimeError

        leadingZeros = nParams[opcode] - len(modes)
        modes = leadingZeros * [0] + modes
        modes.reverse()

        params = list(range(pointer + 1, pointer + 1 + nParams[opcode]))
        for i in range(nParams[opcode]):
            if modes[i] == 0:
                params[i] = intCode[params[i]]

        return (opcode, params)


programs = {
    "ex1": [3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0],
    "ex2": [3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0],
    "ex3": [3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0],
    "ex4": [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5],
    "ex5": [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10],
    "boosters": [3,8,1001,8,10,8,105,1,0,0,21,38,63,72,85,110,191,272,353,434,99999,3,9,102,4,9,9,101,2,9,9,102,3,9,9,4,9,99,3,9,1001,9,4,9,102,2,9,9,1001,9,5,9,1002,9,5,9,101,3,9,9,4,9,99,3,9,1001,9,2,9,4,9,99,3,9,1001,9,3,9,102,2,9,9,4,9,99,3,9,101,2,9,9,102,2,9,9,1001,9,2,9,1002,9,4,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,1,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1001,9,1,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99]
}


def listPrograms(error=False):
    message = "Program not found! Valid program names are:" if error else "Choose a program:"
    
    print("-" * 20)
    print(message)
    for key in programs.keys():
        print("-- " + key)
    print("-" * 20)


def partOne():
    phaseCodes = itertools.permutations(range(0, 5))
    maxThrusters = 0

    for order in phaseCodes:
        thrust = runPhaseCodeSequence(order)
        assert isinstance(thrust, int)
        if thrust > maxThrusters:
            maxThrusters = thrust

    print(maxThrusters)


def runPhaseCodeSequence(seq: tuple[int, ...]):
    res = 0
    for val in seq:
        program = programs["boosters"]
        inputs = [val, res]
        amplifier = intCodeComputer(program)
        res = amplifier.runIntCode(inputs)
    return res


def runFeedbackCodeSequence(seq, programName="boosters"):
    program = programs.get(programName)
    vms = [intCodeComputer(program) for i in range(5)]

    # initialize vms
    for fbc, vm in zip(seq, vms):
        vm.runIntCode([fbc])

    # feedback boosting
    signal = 0
    while True:
        for vm in vms:
            signal: int = vm.runIntCode([signal])
        
        # print(vm.program[vm.pointer], signal)
        
        if vm.program[vm.pointer] == 99: # type: ignore
            break

    # print(signal)
    return signal


def partTwo():
    phaseCodes = itertools.permutations(range(5, 10))
    maxThrusters = 0

    for order in phaseCodes:
        thrust = runFeedbackCodeSequence(order)
        if thrust > maxThrusters:
            maxThrusters = thrust

    print(maxThrusters)

partOne()
partTwo()