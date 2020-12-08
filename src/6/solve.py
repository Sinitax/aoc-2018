from sys import argv as args

f = open("input.txt")
data = f.readlines()
f.close()

def parseEntry(l):
    split = l.split(",")
    return int(split[0]), int(split[1])

data = [parseEntry(l) for l in data if len(l) != 0]

minx = None
miny = None
maxx = None
maxy = None
for c in data:
    if minx == None or c[0] < minx:
        minx = c[0]
    elif maxx == None or c[0] > maxx:
        maxx = c[0]
    if miny == None or c[1] < miny:
        miny = c[1]
    elif maxy == None or c[1] > maxy:
        maxy = c[1]

def getClosest(x,y):
    mc = None
    md = None
    ad = None
    for i in range(len(data)):
        c = data[i]
        dist = abs(c[0] - x) + abs(c[1] - y) # manhattan distance
        if md == None or dist < md:
            md = dist
            mc = i
            ad = None
        elif dist == md:
            ad = dist
    return mc, ad

def getCombinedDist(x,y):
    dist = 0
    for i in range(len(data)):
        c = data[i]
        dist += abs(c[0] - x) + abs(c[1] - y)
    return dist

def solve1():
    areas = dict()
    for x in range(minx, maxx):
        for y in range(miny, maxy):
            mc, ad = getClosest(x, y)

            if ad == None:
                if mc not in areas:
                    areas[mc] = 1
                else:
                    areas[mc] += 1

    # remove outside points

    for i in range(len(data)):
        c = data[i]
        mc, ac = getClosest(minx, c[1])
        if (mc == i):
            areas.pop(i)
            continue
        mc, ac = getClosest(maxx, c[1])
        if (mc == i):
            areas.pop(i)
            continue
        mc, ac = getClosest(c[0], miny)
        if (mc == i):
            areas.pop(i)
            continue
        mc, ac = getClosest(c[0], maxy)
        if (mc == i):
            areas.pop(i)
            continue

    print(max(areas.values()))

def solve2():
    safezone = 0
    for x in range(minx, maxx):
        for y in range(miny, maxy):
            dist = getCombinedDist(x,y)
            if (dist < 10000):
                safezone += 1
    print(safezone)


def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()


