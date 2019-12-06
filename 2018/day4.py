from datetime import datetime
import re
import os
import sys

filePath = os.path.join(sys.path[0], "day4.txt")

events = []

with open(filePath) as file:
    for line in file:
        dateTimeStr, event = line[1:].split("]")
        dateStamp = datetime.strptime(dateTimeStr, '%Y-%m-%d %H:%M')
        event = event.strip()

        events.append((dateStamp, event))

events.sort(key=lambda tup: tup[0])
minutesAsleep = dict()
id = -1
time = -1

for dt, event in events:
    if event[0] == "G":
        id = int(re.sub("[^0-9]", "", event))
        if not id in minutesAsleep:
            minutesAsleep[id] = {}
            for t in range(0, 60):
                minutesAsleep[id][t] = 0
    elif event[0] == "f":
        time = dt.minute
    elif event[0] == "w":
        for t in range(time, dt.minute):
            minutesAsleep[id][t] += 1


def strategy1():

    chosenID = max(minutesAsleep,
                   key=lambda id: sum(minutesAsleep[id].values())
                   )
    chosenMinute = max(minutesAsleep[chosenID],
                       key=lambda m: minutesAsleep[chosenID][m]
                       )
    print(chosenID * chosenMinute)


def strategy2():
    maxAsleep = 0
    chosenMinute = -1
    for id in minutesAsleep:
        maxMinute = max(minutesAsleep[id], key=lambda m: minutesAsleep[id][m])
        print("For id " + str(id) + ": " + str(maxMinute))
        if maxMinute > maxAsleep:
            chosenID, chosenMinute = id, maxMinute

    print(chosenID * chosenMinute)


strategy1()
strategy2()
