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
        while True:
            opcode, par = self.parseInstruction()

            # guarantee write location
            while par and len(self.program) < max(par):
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


programs = {
    "robot": [3,8,1005,8,318,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,0,10,4,10,102,1,8,29,1006,0,99,1006,0,81,1006,0,29,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,59,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,102,1,8,82,1,1103,3,10,2,104,14,10,3,8,102,-1,8,10,101,1,10,10,4,10,108,1,8,10,4,10,102,1,8,111,1,108,2,10,2,1101,7,10,1,1,8,10,1,1009,5,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,102,1,8,149,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,172,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,193,1006,0,39,2,103,4,10,2,1103,20,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,227,1,1106,8,10,2,109,15,10,2,106,14,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,261,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,283,1,1109,9,10,2,1109,5,10,2,1,2,10,1006,0,79,101,1,9,9,1007,9,1087,10,1005,10,15,99,109,640,104,0,104,1,21101,936333124392,0,1,21101,0,335,0,1106,0,439,21102,1,824663880596,1,21102,346,1,0,1105,1,439,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,1,179519553539,1,21101,393,0,0,1106,0,439,21102,46266515623,1,1,21101,0,404,0,1106,0,439,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,983925826324,1,21101,0,427,0,1106,0,439,21101,988220642048,0,1,21102,1,438,0,1105,1,439,99,109,2,21201,-1,0,1,21102,1,40,2,21101,0,470,3,21101,460,0,0,1106,0,503,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,465,466,481,4,0,1001,465,1,465,108,4,465,10,1006,10,497,1101,0,0,465,109,-2,2106,0,0,0,109,4,2102,1,-1,502,1207,-3,0,10,1006,10,520,21101,0,0,-3,22102,1,-3,1,21202,-2,1,2,21102,1,1,3,21102,1,539,0,1105,1,544,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,567,2207,-4,-2,10,1006,10,567,21202,-4,1,-4,1106,0,635,21202,-4,1,1,21201,-3,-1,2,21202,-2,2,3,21102,1,586,0,1105,1,544,21202,1,1,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,605,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,627,21202,-1,1,1,21102,1,627,0,105,1,502,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]
}

UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

TURNL = 0
TURNR = 1

def run(partTwo = False):
    vm = intcodeComputer(programs["robot"])
    pos = (0,0)
    d = UP
    grid = dict()

    if partTwo:
        x, y = pos
        grid[x] = dict()
        grid[x][y] = 1
    rangeX = [0, 1]
    rangeY = [0, 1]
    
    while vm.status != DONE:
        x, y = pos
        if partTwo:
            if x < rangeX[0]:
                rangeX[0] = x
            elif x > rangeX[1]:
                rangeX[1] = x + 1

            if y < rangeY[0]:
                rangeY[0] = y
            elif y > rangeY[1]:
                rangeY[1] = y + 1

        if not x in grid:
            grid[x] = dict()

        if not y in grid[x]:
            grid[x][y] = 0

        col = grid[x][y]
        vm.runIntcode([col])

        grid[x][y], turn = vm.out
        vm.out = []
        d = newDir(d, turn)

        pos = newPos(pos, d)

    tiles = 0
    for x in grid:
        tiles += len(grid[x])

    if not partTwo:
        print("Part One:", tiles)
        return

    lines = dict()
    for x in range(*rangeX):
        for y in range(*rangeY):
            if not y in lines:
                lines[y] = ""

            char = " "
            if x in grid and y in grid[x] and grid[x][y] == 1:
                char = "#"
            
            lines[y] = lines[y] + char

    message = ""

    for i in lines:
        message = lines[i] + "\n" + message 

    print("Part Two: \n", message, sep="")


def newDir(cur, turn):
    if turn == 0: 
        turn = - 1
    
    new = (cur + turn + 4) % 4
    return new

def newPos(pos, d):
    x, y = pos

    if d == UP:
        return (x, y + 1)
    elif d == RIGHT:
        return (x + 1, y)
    elif d == DOWN:
        return (x, y - 1)
    elif d == LEFT:
        return (x - 1, y)
    else:
        print("Error! Invalid new movement? pos, d:", pos, d)
        raise RuntimeError


run()
run(True)