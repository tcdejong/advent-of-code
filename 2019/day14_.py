import os
import sys
from math import ceil
import re


def readInput(filename = "day14.txt"):
    
    filepath = os.path.join(sys.path[0], filename)

    reactions = dict()
    primes = set()

    with open(filepath) as file:
        for reaction in file:
            ingredientsStr, outputStr = reaction.split(sep=" => ")

            outQty, result = outputStr.split(sep=" ")
            result = result.strip()
            components = ingredientsStr.split(sep = ", ")

            ingredients = []
            for component in components:
                qty, name = component.split(" ")
                entry = (int(qty), name.strip())

                if entry[1] == "ORE":
                    primes.add(result)

                ingredients.append( entry )

            reactions[result] = (int(outQty), ingredients)

    return reactions, primes


class PartOne():

    def __init__(self):
        self.inv = dict()

    def reset(self):
        self.inv.clear()

    def oreRequired(self, qty, product):
        reactOut, reactIngred = reactions[product]

        # if reaction requires ore, return required amount
        if len(reactIngred) == 1 and reactIngred[0][1] == "ORE":
            nReactions = ceil(qty / reactOut)
            return reactIngred[0][0] * nReactions
        


        # else: account for current inventory
        if not product in self.inv:
            self.inv[product] = 0
        
        needed = max(qty - self.inv[product], 0)



        # if we already have sufficient in inventory, no extra ore is required
        if needed == 0:
            # remove required from inventory and return 0 ore required
            self.inv[product] -= qty
            return 0



        # if we need to produce components, do so
        nReactions = ceil(needed / reactOut)

        requiredOre = 0
        for (ingrQty, ingrName) in reactIngred:
            requiredOre += nReactions * self.oreRequired(ingrQty, ingrName)

        self.inv[product] += nReactions * reactOut - qty

        return requiredOre

    # def decomposeToPrimes(self, qty, component):
    #     res = dict(zip(primes, [0 for i in primes]))

    #     reactOut, reactIngred = reactions[product]

    #     # if reaction requires ore, return required amount
    #     if len(reactIngred) == 1 and reactIngred[0][1] == "ORE":
    #         nReactions = ceil(qty / reactOut)
    #         return reactIngred[0][0] * nReactions
        
    #     if component in primes:
    #         res[component] += qty
    #     else:
    #         step = self.decomposeToPrimes(qty, component)

    #         for key, val in step:
    #             res[key] += val

    #     return res





reactions, primes = readInput()
partOne = PartOne()
# print(partOne.oreRequired(1, "FUEL"))

assert partOne.oreRequired(1, "GZTS") == 110
partOne.reset()

assert partOne.oreRequired(7, "GSRBL") == 110 
partOne.reset()

assert partOne.oreRequired(8, "GSRBL") == 220 
partOne.reset()

assert partOne.oreRequired(3, "RMQX") == 179
partOne.reset()

assert partOne.oreRequired(3, "BHZP") == 140
partOne.reset()

assert partOne.oreRequired(1, "SFHV") == 3 * 179
partOne.reset()

print("Test:", partOne.oreRequired(1, "FUEL"))
partOne.reset()

print("Fuel:", partOne.oreRequired(1, "FUEL"))
partOne.reset()

# too high:
# 5425025
# 636122
# 420014