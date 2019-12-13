# from ctypes import addressof
from math import gcd

puzzle = '''<x=15, y=-2, z=-6>
<x=-5, y=-4, z=-11>
<x=0, y=-6, z=0>
<x=5, y=9, z=6>'''

ex1 = '''<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>'''

ex2 = '''<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>'''


class Body:
    def __init__(self, x, y, z):
        self.p = {
            "x": x,
            "y": y,
            "z": z
        }
        self.v = {
            "x": 0,
            "y": 0,
            "z": 0
        }

    def __str__(self):
        name = "p = ("
        for axis in self.p:
            name += str(self.p[axis]) + " "
        else:
            name = name.strip()
            name += "),     v = ("

        for axis in self.v:
            name += str(self.v[axis]) + " "
        else:
            name = name.strip()
            name += ")"

        return name

    def applyGravity(self, other):
        for axis in self.p:
            if self.p[axis] < other.p[axis]:
                self.v[axis] += 1
            elif self.p[axis] > other.p[axis]:
                self.v[axis] -= 1

    def applyVelocity(self):
        for axis in self.p:
            self.p[axis] += self.v[axis]

    def potE(self):
        return sum([abs(i) for i in self.p.values()])

    def kinE(self):
        return sum([abs(i) for i in self.v.values()])

    def totE(self):
        return self.potE() * self.kinE()


def createBodies(inputStr):
    lineLists = [l[1:-1].split(",") for l in inputStr.splitlines()]

    bodies = []
    for line in lineLists:
        x = int(line[0].strip()[2:])
        y = int(line[1].strip()[2:])
        z = int(line[2].strip()[2:])
        bodies.append(Body(x, y, z))

    return bodies


def partOne(inputStr):
    bodies = createBodies(inputStr)
    for t in range(1, 1000 + 1):
        for body in bodies:
            for other in bodies:
                if body == other:
                    continue
                body.applyGravity(other)

        if t % 100 == 0:
            print("-" * 20)
            print("After", t, "steps:")
        for body in bodies:
            body.applyVelocity()
            if t % 100 == 0:
                print(body)

    else:
        total = sum([b.totE() for b in bodies])

    print(total)


def partTwo(inputStr):
    bodies = createBodies(inputStr)
    state0 = dict()

    cycletime = dict()

    t = 0
    while True:
        for body in bodies:
            for other in bodies:
                if body == other:
                    continue
                body.applyGravity(other)

        for body in bodies:
            body.applyVelocity()

        for axis in ["x", "y", "z"]:
            if axis in cycletime:
                continue

            state = [(body.p[axis], body.v[axis]) for body in bodies]
            state = tuple(state)

            if t == 0:
                state0[axis] = state
            elif state == state0[axis]:
                cycletime[axis] = t
                continue

        if len(cycletime) == 3:
            print(cycletime)
            break

        t += 1

    times = list(cycletime.values())
    print(lcm(times))


def lcm(args):
    if len(args) == 2:
        a, b = args

        if a == b:
            return a

        return abs(a * b) // gcd(a, b)

    else:
        res = args[0]
        for i in args:
            res = lcm([res, i])
        return res


partOne(puzzle)
partTwo(puzzle)

# times = [161428, 167624, 193052]
# print(lcm(times))
