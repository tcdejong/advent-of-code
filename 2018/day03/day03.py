import os
import sys

inputPath = os.path.join(sys.path[0], "day3.txt")

BIT_SHIFT = 10


def parseClaim(line="#1353 @ 16,25: 17x10"):
    # Claim format: #1353 @ 16,25: 17x10
    # A claim like #123 @ 3,2: 5x4 means that claim ID 123 specifies a rectangle 3 inches from the left edge,
    # 2 inches from the top edge, 5 inches wide, and 4 inches tall.

    line = line[1:].strip()

    id, trash, remainder = line.partition("@")
    margin, trash, dim = remainder.partition(":")
    left, trash, top = margin.partition(",")
    width, trash, height = dim.partition("x")
    del trash

    id = int(id)
    left = int(left)
    top = int(top)
    width = int(width)
    height = int(height)

    return [id, (left, top, width, height)]


def bundleXY(x, y):
    x = x << BIT_SHIFT
    res = x | y
    return res


def unbundleXY(xy):
    mask = int('00000000001111111111', 2)
    y = xy & mask
    x = xy & ~mask
    x = x >> BIT_SHIFT
    return (x, y)


def partOne():
    # We do not need ids for part 1.
    # This can change to use a dictionary when we do.

    claims = []
    with open(inputPath) as rawData:
        for line in rawData:
            claim = parseClaim(line)
            claims.append(claim[1])

    seen = set()
    overlap = set()

    for claim in claims:
        for x in range(claim[0], claim[0] + claim[2]):
            for y in range(claim[1], claim[1] + claim[3]):
                bundled = bundleXY(x, y)
                if bundled in seen:
                    overlap.add(bundled)
                else:
                    seen.add(bundled)

    print("Square inches of overlap: ", len(overlap), sep=" ")


partOne()


def partTwo():
    claims = dict()
    with open(inputPath) as rawData:
        for line in rawData:
            claim = parseClaim(line)
            claims[claim[0]] = (claim[1])

    seen = set()
    overlap = set()

    for id in claims.keys():
        claim = claims.get(id)
        assert claim
        for x in range(claim[0], claim[0] + claim[2]):
            for y in range(claim[1], claim[1] + claim[3]):
                bundled = bundleXY(x, y)
                if bundled in seen:
                    overlap.add(bundled)
                else:
                    seen.add(bundled)

    for id in claims.keys():
        claim = claims.get(id)
        assert claim
        
        overlaps = False
        for x in range(claim[0], claim[0] + claim[2]):
            for y in range(claim[1], claim[1] + claim[3]):
                bundled = bundleXY(x, y)
                if bundled in overlap:
                    overlaps = True
                    break
            if overlaps == True:
                break
        if overlaps == True:
            continue
        else:
            print("Non-overlapping claim has id:", id, sep=" ")
            return id


partTwo()
