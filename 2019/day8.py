import os
import sys

filepath = os.path.join(sys.path[0], "day8.txt")

with open(filepath) as file:
    dataRaw = list(file.read().strip())
    data = list(map(int, dataRaw))

def getLayers(w, h):
    layers = dict()
    numLayers = len(data) // (w*h)

    for i in range(numLayers):
        start = i * w * h
        end = start + w * h
        layers[i] = data[start:end]

    return layers


def partOne(w, h):
    layers = getLayers(w, h)
    leastZeros = w * h
    for layer in layers.values():
        zeros = layer.count(0)
        if zeros < leastZeros:
            leastZeros, ones, twos = zeros, layer.count(1), layer.count(2)
    print(ones * twos)


def partTwo(w, h):
    layers = getLayers(w, h)
    res = {}

    for y in range(h):
        if not y in res:
                res[y] = dict()

        for x in range(w):
            # for l in range(toplayer, -1, -1):
            for l in layers:
                pxl = layers[l][x + y * w]
                if pxl != 2:
                    res[y][x] = pxl
                    break
    
    printMessage(res)


def printMessage(res):
    message = ""
    for y in res:
        for x in res[y]:
            c = res[y][x]
            c = c if c == 1 else " "
            message += str(c)
        
        message += "\n"


    print(message)


# partOne(25, 6)
partTwo(25, 6)