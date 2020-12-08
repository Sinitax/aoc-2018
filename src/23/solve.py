# 2nd part solved with the help of subreddit

from sys import argv as args
import math

# read input file
file = open("input.txt")
sinput = file.read()
file.close()

# nanobots consist of tuples containing: (position, radius)
nanobots = list()

# parse a line of input file
def parseLine(l):
    s = l.split(">, ")
    pos = [int(v) for v in s[0].split("=<")[1].split(",")]
    radius = int(s[1].split("=")[1])
    nanobots.append((pos, radius))

# parse input file
sinput = [parseLine(l) for l in sinput.split("\n") if len(l) != 0]

# manhattan distance
def dist(p1, p2):
    xd = abs(p1[0] - p2[0])
    yd = abs(p1[1] - p2[1])
    zd = abs(p1[2] - p2[2])
    return xd + yd + zd

# two nanobots range overlap
def isoverlap(nb1, nb2):
    return nb1[1] + nb2[1] >= dist(nb1[0], nb2[0])

# nanobots range completely inside anothers range
def isinside(nb1, nb2):
    return dist(nb1[0], nb2[0]) <= nb2[1] - nb1[1]

# check if range of nanobot is inside grid
def tileinrange(tile, nb, gridsize):
    hgridsize = math.floor(gridsize / 2) # case gridsize = 1 => squares should have 0 width
    nbp = nb[0]
    ds = [abs(nbp[i] - tile[i]) for i in range(3)]
    md = max(ds)
    if md == 0:
        return True
    ds = [d * hgridsize / md for d in ds] # get distance along squares sides
    return dist(nbp, tile) - sum(ds) <= nb[1]

### PROGRAM CODE

def solve1():
    maxr = max(nanobots, key = lambda x : x[1])
    inrange = 0
    for nb in nanobots:
        if dist(nb[0], maxr[0]) <= maxr[1]:
            inrange += 1
    print(inrange)

def solve2():
    global nanobots
    # use smaller getting grid like binary search to find position in range of most nanobots
    minpx = min(nanobots, key = lambda x : x[0][0])[0][0]
    minpy = min(nanobots, key = lambda x : x[0][1])[0][1]
    minpz = min(nanobots, key = lambda x : x[0][2])[0][2]
    minp = (minpx, minpy, minpz)

    maxpx = max(nanobots, key = lambda x : x[0][0])[0][0]
    maxpy = max(nanobots, key = lambda x : x[0][1])[0][1]
    maxpz = max(nanobots, key = lambda x : x[0][2])[0][2]
    maxp = (maxpx, maxpy, maxpz)

    gridsize = max([maxp[i] - minp[i] for i in range(3)]) # largest dif dim to ensure all nanbots are in the grid

    bestpos = None
    while gridsize >= 1:
        maxintile = 0

        # traverse grid in steps of gridsize
        xsteps = math.ceil((maxp[0] - minp[0]) / gridsize) + 1
        ysteps = math.ceil((maxp[1] - minp[1]) / gridsize) + 1
        zsteps = math.ceil((maxp[2] - minp[2]) / gridsize) + 1
        for nx in range(xsteps):
            for ny in range(ysteps):
                for nz in range(zsteps):
                    x = minp[0] + nx * gridsize
                    y = minp[1] + ny * gridsize
                    z = minp[2] + nz * gridsize
                    intile = 0
                    for nb in nanobots:
                        if tileinrange((x, y, z), nb, gridsize): # check if nanobots range intersects with tile
                            intile += 1
                    if maxintile < intile:
                        maxintile = intile
                        bestpos = (x, y, z)
                    elif maxintile == intile:
                        if maxintile == 0 or sum([abs(v) for v in (x, y, z)]) < sum([abs(v) for v in bestpos]): # if two gridtiles have the same count, choose the one closest to the origin
                            bestpos = (x, y, z)

        if gridsize == 1:
            break
        gridsize = math.floor(gridsize / 2)

        minp = [v - gridsize for v in bestpos]
        maxp = [v + gridsize for v in bestpos]

    print(sum(bestpos))

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
