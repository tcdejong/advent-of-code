from copy import deepcopy

# opcodes
ADD = 1
MULT = 2
INP = 3
OUTP = 4
JIFT = 5
JIFF = 6
LT = 7
EQ = 8
RELB = 9
HALT = 99

# Number of parameters per opcode
nParams = {
    ADD: 3,
    MULT: 3,
    INP: 1,
    OUTP: 1,
    JIFT: 2,
    JIFF: 2,
    LT: 3,
    EQ: 3,
    RELB: 1,
    HALT: 0,
}

# intcodeComputer status codes
READY = 0
NEED_INPUT = 1
DONE = 2
ERR_OPCODE = -1

class intcodeComputer:
    def __init__(self, program, pointer=0, relBase=0):
        self.program = deepcopy(program)
        self.pointer = deepcopy(pointer)
        self.relBase = 0
        self.inp = []
        self.out = []
        self.status = READY

    def test(self):
        return self.pointer

    def runIntcode(self, inputs):
        # inputs = cleanInputs(inputs)
        while True:
            opcode, par = self.parseInstruction()

            # guarantee write location
            while par and len(self.program) < max(par) - 1:
                self.program = self.program + ([0] * 1000)

            # process opcode
            if opcode == ADD:
                self.program[par[2]] = self.program[par[0]] + self.program[par[1]]
            elif opcode == MULT:
                self.program[par[2]] = self.program[par[0]] * self.program[par[1]]
            elif opcode == INP:
                if len(inputs) == 0:
                    self.status = NEED_INPUT
                    break
                self.program[par[0]] = inputs.pop(0)
            elif opcode == OUTP:
                self.out.append(self.program[par[0]])
            elif opcode == JIFT:
                if self.program[par[0]] != 0:
                    self.pointer = self.program[par[1]]
                    continue
            elif opcode == JIFF:
                if self.program[par[0]] == 0:
                    self.pointer = self.program[par[1]]
                    continue
            elif opcode == LT:
                self.program[par[2]] = 1 if self.program[par[0]] < self.program[par[1]] else 0
            elif opcode == EQ:
                self.program[par[2]] = 1 if self.program[par[0]] == self.program[par[1]] else 0
            elif opcode == RELB:
                self.relBase += self.program[par[0]]
            elif opcode == HALT:
                self.status = DONE
                break
            else:
                self.status = ERR_OPCODE
                break

            self.pointer += nParams[opcode] + 1

        return self.out

    def parseInstruction(self):
        intCode = self.program
        pointer = self.pointer
        instruction = intCode[pointer]
        digits = list(map(int, list(str(instruction))))  # Ew
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
            mode = modes[i]
            if mode == 0:
                params[i] = intCode[params[i]]
            elif mode == 1:
                continue
            elif mode == 2:
                params[i] = intCode[params[i]] + self.relBase

        return (opcode, params)


def listPrograms(error=False):
    message = "Program not found! Valid program names are:" if error else "Choose a program:"
    print("-" * 20)
    print(message)
    for key in programs.keys():
        print("-- " + key)
    print("-" * 20)


programs = {
    "ex1": [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99],
    "ex2": [1102,34915192,34915192,7,4,7,99,0],
    "ex3": [104,1125899906842624,99],
    "challenge": [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1101,0,3,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1102,23,1,1004,1102,1,26,1000,1102,897,1,1028,1101,27,0,1012,1102,33,1,1001,1102,32,1,1007,1101,39,0,1005,1101,0,29,1018,1101,0,0,1020,1101,1,0,1021,1101,0,21,1002,1102,1,35,1014,1101,0,36,1009,1102,1,38,1006,1102,1,251,1024,1102,28,1,1017,1102,37,1,1008,1102,1,329,1026,1102,25,1,1011,1102,31,1,1013,1102,892,1,1029,1102,242,1,1025,1102,1,881,1022,1102,22,1,1003,1102,874,1,1023,1101,20,0,1016,1101,24,0,1019,1101,0,326,1027,1101,0,34,1015,1102,1,30,1010,109,-2,2102,1,7,63,1008,63,36,63,1005,63,205,1001,64,1,64,1105,1,207,4,187,1002,64,2,64,109,9,21101,40,0,6,1008,1013,43,63,1005,63,227,1105,1,233,4,213,1001,64,1,64,1002,64,2,64,109,26,2105,1,-9,4,239,1001,64,1,64,1106,0,251,1002,64,2,64,109,-15,1205,2,263,1105,1,269,4,257,1001,64,1,64,1002,64,2,64,109,-9,2102,1,0,63,1008,63,36,63,1005,63,295,4,275,1001,64,1,64,1106,0,295,1002,64,2,64,109,-14,1207,10,38,63,1005,63,311,1105,1,317,4,301,1001,64,1,64,1002,64,2,64,109,28,2106,0,4,1106,0,335,4,323,1001,64,1,64,1002,64,2,64,109,-8,1206,6,351,1001,64,1,64,1106,0,353,4,341,1002,64,2,64,109,-1,2107,33,-7,63,1005,63,369,1106,0,375,4,359,1001,64,1,64,1002,64,2,64,109,-9,2108,26,-1,63,1005,63,395,1001,64,1,64,1106,0,397,4,381,1002,64,2,64,109,3,1201,-2,0,63,1008,63,38,63,1005,63,419,4,403,1105,1,423,1001,64,1,64,1002,64,2,64,109,-13,2101,0,9,63,1008,63,23,63,1005,63,445,4,429,1105,1,449,1001,64,1,64,1002,64,2,64,109,11,1208,1,32,63,1005,63,471,4,455,1001,64,1,64,1106,0,471,1002,64,2,64,109,17,21108,41,38,-4,1005,1019,487,1105,1,493,4,477,1001,64,1,64,1002,64,2,64,109,6,1206,-9,511,4,499,1001,64,1,64,1106,0,511,1002,64,2,64,109,-23,21102,42,1,8,1008,1014,42,63,1005,63,533,4,517,1106,0,537,1001,64,1,64,1002,64,2,64,109,-3,2107,36,5,63,1005,63,555,4,543,1106,0,559,1001,64,1,64,1002,64,2,64,109,-6,1202,5,1,63,1008,63,21,63,1005,63,581,4,565,1106,0,585,1001,64,1,64,1002,64,2,64,109,1,1208,10,40,63,1005,63,605,1001,64,1,64,1106,0,607,4,591,1002,64,2,64,109,7,1201,0,0,63,1008,63,42,63,1005,63,631,1001,64,1,64,1106,0,633,4,613,1002,64,2,64,109,1,21107,43,42,7,1005,1013,649,1105,1,655,4,639,1001,64,1,64,1002,64,2,64,109,7,21108,44,44,3,1005,1016,677,4,661,1001,64,1,64,1106,0,677,1002,64,2,64,109,-7,21102,45,1,9,1008,1015,44,63,1005,63,701,1001,64,1,64,1106,0,703,4,683,1002,64,2,64,109,13,21101,46,0,-7,1008,1012,46,63,1005,63,729,4,709,1001,64,1,64,1105,1,729,1002,64,2,64,109,-13,2101,0,3,63,1008,63,33,63,1005,63,753,1001,64,1,64,1106,0,755,4,735,1002,64,2,64,109,14,1205,1,773,4,761,1001,64,1,64,1105,1,773,1002,64,2,64,109,-23,1202,10,1,63,1008,63,30,63,1005,63,797,1001,64,1,64,1105,1,799,4,779,1002,64,2,64,109,13,2108,22,-7,63,1005,63,817,4,805,1106,0,821,1001,64,1,64,1002,64,2,64,109,-11,1207,5,24,63,1005,63,843,4,827,1001,64,1,64,1105,1,843,1002,64,2,64,109,11,21107,47,48,7,1005,1017,861,4,849,1106,0,865,1001,64,1,64,1002,64,2,64,109,15,2105,1,-2,1001,64,1,64,1106,0,883,4,871,1002,64,2,64,109,10,2106,0,-7,4,889,1106,0,901,1001,64,1,64,4,64,99,21102,1,27,1,21102,1,915,0,1105,1,922,21201,1,28510,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,1,942,0,1106,0,922,22102,1,1,-1,21201,-2,-3,1,21101,957,0,0,1106,0,922,22201,1,-1,-2,1105,1,968,21202,-2,1,-2,109,-3,2106,0,0]
}

def run(inp):
    vm = intcodeComputer(programs["challenge"])
    vm.runIntcode([inp])
    print(vm.out)


run(1)
run(2)
