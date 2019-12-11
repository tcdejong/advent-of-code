from string import ascii_uppercase
import os
import sys


def loadInput():
    filePath = os.path.join(sys.path[0], "day7.txt")

    dependencies = dict()

    with open(filePath) as file:
        for line in file:
            predecessor = line[5]
            activity = line[36]

            if not predecessor in dependencies:
                dependencies[predecessor] = set()
            if not activity in dependencies:
                dependencies[activity] = set()

            dependencies[activity].add(predecessor)

    return dependencies


def partOne():
    dependencies = loadInput()

    res = ""

    while dependencies:
        validSteps = [act for act in dependencies if len(
            dependencies[act]) == 0]
        validSteps.sort()

        act = validSteps[0]
        res += act

        for dep in dependencies:
            if act in dependencies[dep]:
                dependencies[dep].remove(act)

        del dependencies[act]

    print(res)


def partTwo():
    letterCost = dict(zip(ascii_uppercase, range(1, 27)))
    dependencies = loadInput()

    res = ""

    t = 0
    w = 5
    wFreeAt = ([0] * w)
    wTask = ([""] * w)

    while dependencies:
        # process finished jobs
        freeWorkers = []
        done = set()
        for i in range(w):
            if wFreeAt[i] <= t:
                freeWorkers.append(i)
                act = wTask[i]
                if act == "":
                    continue
                done.add(act)
                wTask[i] = ""

        if len(done):
            for dep in dependencies:
                dependencies[dep] = dependencies[dep] - done
            for act in done:
                res += act
                if act in dependencies:
                    del dependencies[act]

        # determine available jobs
        validSteps = [act for act in dependencies if len(
            dependencies[act]) == 0 and not act in wTask]
        validSteps.sort()

        # limit jobs based on current availability of workers and finished predecessors
        newJobs = min(len(freeWorkers), len(validSteps))

        # assign new jobs
        for i in range(newJobs):
            act = validSteps[i]
            cost = 60 + letterCost[act]
            id = freeWorkers[i]
            wTask[id], wFreeAt[id] = act, t + cost

        jump = max(wFreeAt)
        for i in wFreeAt:
            if i > t and i < jump:
                jump = i
        t = jump

    print(t)


partOne()
partTwo()
