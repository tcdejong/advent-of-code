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


# TODO Add tests using `assert` and previous challenge inputs
# TODO implement class in challenges prior to day 13


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

    def runIntcode(self, inputs=[]):
        while True:
            opcode, par = self.parseInstruction()

            # guarantee write location
            while par and len(self.program) < max(par):
                self.program = self.program + ([0] * 1000)

            # process opcode
            if opcode == ADD:
                self.program[par[2]] = self.program[par[0]] + \
                    self.program[par[1]]
            elif opcode == MULT:
                self.program[par[2]] = self.program[par[0]] * \
                    self.program[par[1]]
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
                self.program[par[2]] = 1 if self.program[par[0]
                                                         ] < self.program[par[1]] else 0
            elif opcode == EQ:
                self.program[par[2]] = 1 if self.program[par[0]
                                                         ] == self.program[par[1]] else 0
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
            raise ValueError

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
