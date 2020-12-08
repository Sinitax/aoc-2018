from sys import argv as args

debug = False

def parseLine(l):
    s = l.split(", ")
    if s[0].startswith("y="):
        s = s[::-1]

    res = [[int(x) for x in v.split("=")[1].split("..")] for v in s]
    return res

file = open("input.txt")
sinput = file.read()
file.close()

ainput = """x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504"""

sinput = [l for l in sinput.split("\n") if len(l) != 0]

constraints = [parseLine(l) for l in sinput]

xmin = min(c[0][0] for c in constraints)-1
xmax = max(c[0][-1] for c in constraints)+1
ymin = min(c[1][0] for c in constraints)
ymax = max(c[1][-1] for c in constraints)
xdif = xmax - xmin + 1
ydif = ymax - ymin + 1

#print(xmin, xmax)
#print(ymin, ymax)

vmap = [[0 for x in range(xdif)] for y in range(ydif)]

def setMap(x, y, v):
    global vmap
    if y < ymin or y > ymax or x < xmin or x > xmax:
        return
    vmap[y-ymin][x-xmin] = v

def getMap(x, y):
    global vmap
    if x > xmax or x < xmin:
        return 1
    elif y > ymax:
        return 0
    return vmap[y-ymin][x-xmin]

def drawWall(c):
    if len(c[0]) == 1:
        for y in range(c[1][0], c[1][1] + 1):
            setMap(c[0][0], y, 1)
    else:
        for x in range(c[0][0], c[0][1] + 1):
            setMap(x, c[1][0], 1)

for c in constraints:
    drawWall(c)

spring = (500, 0)


### SETUP END


def interpretChar(v):
    chars = [".", "#", "|", "~"]
    return chars[v]

def drawMap():
    for y in range(ydif):
        print("".join([interpretChar(v) for v in vmap[y]]))

def fwriteMap():
    f = open("output","w+")
    for y in range(ydif):
        f.write("".join([interpretChar(v) for v in vmap[y]])+"\n")
    f.close()

def isstatic(p):
    return getMap(p[0], p[1]) in (1, 3)

def isfree(p):
    return getMap(p[0], p[1]) == 0

def move(p):
    x = p[0]
    y = p[1]
    if isfree((x, y+1)):
        return (x, y+1)
    onblock = isstatic((x, y+1))
    if not onblock:
        return (x,y)
    npos = [(x + dir, y) for dir in [-1, 1]]
    npos = [np for np in npos if isfree(np) and onblock]
    if len(npos) > 1:
        return npos
    elif len(npos) == 1:
        return npos[0]
    return (x, y)

def fillfloor(p):
    onblock = True
    isblock = False
    x = p[0]
    while onblock and not isblock and x >= xmin:
        x -= 1
        isblock = isstatic((x, p[1]))
        onblock = isstatic((x, p[1]+1))
    if not isblock:
        return None # edge
    lx = x+1

    onblock = True
    isblock = False
    x = p[0]
    while onblock and not isblock and x <= xmax:
        x += 1
        isblock = isstatic((x, p[1]))
        onblock = isstatic((x, p[1]+1))
    if not isblock:
        return None
    rx = x-1

    return [(i, p[1]) for i in range(lx, rx+1)]

def countWFlowing():
    water = 0
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            if getMap(x,y) == 2:
                water += 1
    return water

def countWStatic():
    water = 0
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            if getMap(x,y) == 3:
                water += 1
    return water

def simulate():
    heads = [spring]
    while len(heads) > 0:
        cp = heads[-1]
        if isstatic((cp[0], cp[1]+1)):
            # solid below => expand
            res = fillfloor(cp)
            if res:
                for p in res:
                    setMap(p[0], p[1], 3)
                nhead = None
                for x in range(res[0][0], res[-1][0]+1):
                    np = (x, res[0][1]-1)
                    if getMap(np[0], np[1]) == 2:
                        nhead = np
                        break
                if nhead == None: # head got trapped
                    heads.pop()
                else:
                    heads[-1] = nhead
                continue

        res = move(cp)
        if type(res[0]) == tuple:
            heads.pop()
            heads += res
            for p in res:
                setMap(p[0], p[1], 2)
        else:
            if res != cp:
                if res[1] <= ymax:
                    setMap(res[0], res[1], 2)
                    heads[-1] = res
                else:
                    heads.pop()
            else:
                heads.pop()

        if debug:
            print(heads)
            input()
            fwriteMap()

def solve1():
    simulate()
    #fwriteMap()
    print(countWFlowing() + countWStatic())
    return

def solve2():
    simulate()
    #fwriteMap()
    print(countWStatic())
    return

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
