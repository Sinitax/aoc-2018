def parseLine(l):
    s = l.split(">")
    vals = list()
    for ss in s:
        if len(ss) == 0:
            continue
        ss = ss.split("<",1)[1]
        vals.append([int(x) for x in ss.split(",")])
    return vals

data = [parseLine(l) for l in open("input.txt").read().split("\n") if len(l) != 0]
posdata = [x[0] for x in data]
veldata = [x[1] for x in data]

def checkAdjacent(pi):
    for p in posdata:
        if abs(p[0] - pi[0]) + abs(p[1] - pi[1]) == 1:
            return True
    return False

def checkData():
    for p in posdata:
        if not checkAdjacent(p):
            return False
    return True

def calcMax():
    minx = None
    maxx = None
    miny = None
    maxy = None
    for p in posdata:
        if minx is None or p[0] < minx:
            minx = p[0]
        if maxx is None or p[0] > maxx:
            maxx = p[0]
        if miny is None or p[1] < miny:
            miny = p[1]
        if maxy is None or p[1] > maxy:
            maxy = p[1]
    return minx, maxx, miny, maxy

def solveBoth():
    count = 0
    distx = None
    disty = None
    while True:
        for i in range(len(data)):
            posdata[i][0] += veldata[i][0]
            posdata[i][1] += veldata[i][1]
        count += 1

        minx, maxx, miny, maxy = calcMax()
        if distx == None:
            distx = maxx - minx
            disty = maxy - miny
        else:
            cdistx = maxx - minx
            cdisty = maxy - miny
            if cdistx > distx or cdisty > disty:
                for i in range(len(data)):
                    posdata[i][0] -= veldata[i][0]
                    posdata[i][1] -= veldata[i][1]
                count -= 1
                break
            else:
                distx = cdistx
                disty = cdisty

        if count % 100 == 0:
            print("\r" + " " * 50, end="")
            print(f"\rcluster size: {distx}, {disty}", end="")

    print("\r" + " " * 50 + "\r", end="")
    print("part 1: " + str(count))
    minx, maxx, miny, maxy = calcMax()
    print("part 2: ");
    for y in range(maxy - miny + 1):
        print("".join([("#" if list([x + minx, y + miny]) in posdata else " ") for x in range(maxx - minx + 1)]))

solveBoth()
