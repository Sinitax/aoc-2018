from sys import argv as args
from copy import deepcopy
from collections import deque

states = (".", "|", "#")

ivals = dict()
ivals["#"] = 0
ivals["."] = 0
ivals["|"] = 0

def parseLine(l):
    return tuple([states.index(c) for c in l])

inputstr = open("input.txt").read()

sinputstr = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""

vmap = [parseLine(l) for l in inputstr.split("\n") if len(l) != 0]
ylen = len(vmap)
xlen = len(vmap[0])

def getAt(x, y):
    if y < 0 or y >= ylen or x < 0 or x >= xlen:
        return None
    return vmap[y][x]

def next(x, y):
    v = vmap[y][x]
    around = list()
    [[around.append(getAt(x+i-1, y+j-1)) for j in range(3) if not (i == 1 and j == 1)] for i in range(3)]
    if v == 0:
        if len([v for v in around if v == 1]) >= 3:
            return 1
    elif v == 1:
        if len([v for v in around if v == 2]) >= 3:
            return 2
    elif v == 2:
        if len([v for v in around if v == 1]) < 1 or len([v for v in around if v == 2]) < 1:
            return 0
    return v

def getVals():
    vals = [0 for x in range(3)]
    for y in range(ylen):
        for x in range(xlen):
            vals[vmap[y][x]] += 1
    return vals

def drawMap(cmap):
    for y in range(ylen):
        print("".join([str(c) for c in cmap[y]]))

def iterate(n):
    global vmap
    for i in range(n):
        omap = [deque() for y in range(ylen)]
        for y in range(ylen):
            for x in range(xlen):
                omap[y].append(next(x, y))
        vmap = omap

def getRes():
    vals = getVals()
    return (vals[1] * vals[2])

def solve1():
    #drawMap(vmap)
    iterate(10)
    vals = getVals()
    #drawMap(vmap)
    print(vals[1] * vals[2])
    return

def solve2():
    iterate(1000)
    omap = deepcopy(vmap)
    counter = 0
    while True:
        iterate(1)
        counter += 1
        if vmap == omap:
            break

    #print(counter)
    print(getRes())
    #drawMap(vmap)
    return

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
