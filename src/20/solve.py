from sys import argv as args
from copy import deepcopy

sinput = list(open("input.txt").read().strip())

ainput = "^ENWWW(NEEE|SSE(EE|N))$"

def getMap(p):
    return vmap[p[1] + spos[1]][p[0] + spos[0]]

def setMap(p, c):
    global vmap, spos
    vmap[p[1] + spos[1]][p[0] + spos[0]] = c

def newpos(p, c):
    p = p[:]
    if c == "N":
        p[1] -= 2
    elif c == "S":
        p[1] += 2
    elif c == "W":
        p[0] -= 2
    elif c == "E":
        p[0] += 2
    return p

def calcpos(stack):
    p = [0,0]
    for c in stack:
        p = newpos(p, c)
    return p

xmin = 0
xmax = 0
ymin = 0
ymax = 0

def checkSize(stack):
    global xmin, xmax, ymin, ymax
    p = calcpos(stack)
    if p[0] < xmin:
        xmin = p[0]
    if p[0] > xmax:
        xmax = p[0]
    if p[1] < ymin:
        ymin = p[1]
    if p[1] > ymax:
        ymax = p[1]

def drawRoute(stack):
    p = calcpos(stack)
    setMap(p, ".")
    np = newpos(p, stack[-1])
    cp = [0,0]
    cp[0] = p[0] + int((p[0] - np[0])/2)
    cp[1] = p[1] + int((p[1] - np[1])/2)
    setMap(cp, "+")

def iterRegex(func):
    stacklens = [0]
    stack = []
    for i in range(1, len(sinput)-1):
        c = sinput[i]
        if c == "(":
            stacklens.append(0)
        elif c == "|":
            for i in range(stacklens[-1]):
                stack.pop()
            stacklens[-1] = 0
        elif c == ")":
            for i in range(stacklens[-1]):
                stack.pop()
            stacklens.pop()
        else:
            stack.append(c)
            stacklens[-1] += 1
            func(stack)

def fwriteMap():
    f = open("output", "w+")
    for y in range(len(vmap)):
        f.write("".join([str(v) for v in vmap[y]]) + "\n")
    f.close()

mshape = None
spos = None
vmap = None

def genMap():
    global vmap, mshape, spos
    iterRegex(checkSize)
    xdif = xmax - xmin + 2
    ydif = ymax - ymin + 2

    spos = (-xmin+1, -ymin+1)
    mshape = (xdif, ydif)

    vmap = [["#" for x in range(xdif+1)] for y in range(ydif+1)]
    vmap[spos[1]][spos[0]] = "X"

    iterRegex(drawRoute)


adjacent = ((-1, 0), (0, -1), (1, 0), (0, 1))

def genCountmap(sp):
    countmap = dict()
    next = dict()
    next[(sp[0], sp[1])] = 0
    counter = 0
    steps = list()
    while len(next) > 0 and len(steps) == 0: # first steps available will be shortest
        countmap = {**countmap, **next} # merge dictionaries
        counter += 1
        temp = dict()
        for n in next:
            for dir in adjacent:
                nx = n[0]+dir[0]
                ny = n[1]+dir[1]
                if getMap((nx, ny)) != "#" and (nx, ny) not in countmap and (nx, ny) not in temp:
                    temp[(nx,ny)] = counter
        next = temp
    return countmap

def nextStep(cmap, p):
    # adjacent squares
    npos = [[p[0] + dir[0], p[1] + dir[1]] for dir in adjacent]

    # steps and dist
    steps = [[np[0], np[1], cmap[np[0], np[1]]] for np in npos if (np[0], np[1]) in cmap]

    if len(steps) == 0:
        return None
    else:
        return sorted(steps, key = lambda x: x[2])[0] #closest

### SETUP

genMap()
#print("finished generating..")

### PROBLEM CODE

def solve1():
    cmap = genCountmap((0,0))
    ipos = sorted(cmap, key = lambda x : cmap[x])[-1]
    print(int(cmap[ipos]/2))
    #fwriteMap()
    return

def solve2():
    cmap = genCountmap((0,0))
    count = len([v for v in cmap if int(cmap[v]/2) >= 1000 and getMap(v) == "."])
    print(count)
    return

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
