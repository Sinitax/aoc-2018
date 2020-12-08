from sys import argv as args

debug = False

file = open("input.txt")
input = file.readlines()
file.close()

#sample 1 - (works!)
ainput = """#######
#G..#E#
#E#E.E#
#G.##.#
#...#E#
#...E.#
#######""".split("\n")

#sample 2 - (works!)
binput = """#######
#E..EG#
#.#G.E#
#E.##E#
#G..#.#
#..E#.#
#######""".split("\n")

#sample 3 - (works!)
cinput = """#######
#E.G#.#
#.#G..#
#G.#.G#
#G..#.#
#...E.#
#######""".split("\n")

#sample 4 - (works!)
dinput = """#######
#.E...#
#.#..G#
#.###.#
#E#G#G#
#...#G#
#######""".split("\n")

#sample 5 - (works!)
einput = """#########
#G......#
#.E.#...#
#..##..G#
#...##..#
#...#...#
#.G...G.#
#.....G.#
#########""".split("\n")

#sample 6 - (works!)
finput = """#######
#.G...#
#...EG#
#.#.#G#
#..G#E#
#.....#
#######""".split("\n")

sinput = dinput

actors = list()
input = [l.replace("\n","") for l in input]

def parseEntity(x, y):
    global actors
    c = input[y][x]
    if c == "#":
        return 1
    else:
        if c == "G":
            actors.append([x, y, 200, 1, len(actors), 3])
        elif c == "E":
            actors.append([x, y, 200, 0, len(actors), 3])
        return 0

ylen = len(input)
xlen = len(input[0])

adjacent = [[0, -1], [-1, 0], [1, 0], [0, 1]] # first in reading order
vmap = list()

def setGame():
    global vmap, actors
    actors = list()
    vmap = [[parseEntity(x, y) for x in range(xlen)] for y in range(ylen)]


def inmap(cmap, cx, cy):
    for i in range(len(cmap)):
        ent = cmap[i]
        if ent[0] == cx and ent[1] == cy:
            return i
    return None

def iswall(x,y):
    return vmap[y][x] != 0

def isblocked(x, y):
    return (vmap[y][x] != 0 or inmap(actors, x, y) != None)

def freeAdjacent(x, y):
    poslist = list()
    for dir in adjacent:
        nx = x + dir[0]
        ny = y + dir[1]
        if not isblocked(nx, ny):
            poslist.append((nx,ny))
    return poslist

def flatten(l):
    flat = list()
    for ll in l:
        flat += ll
    return flat

def drawMap():
    global actors
    for y in range(ylen):
        for x in range(xlen):
            ind = inmap(actors, x, y)
            print(("G" if actors[ind][3] == 1 else "E") if ind != None else ("." if vmap[y][x] == 0 else "#"), end="")
        print()

def getSteps(cmap, a1):
    # adjacent squares
    npos = [[a1[0] + dir[0], a1[1] + dir[1]] for dir in adjacent]

    # pos of enemy and distance
    steps = [[np[0], np[1], cmap[np[0], np[1]]] for np in npos if (np[0], np[1]) in cmap]

    return steps

def closestStep(a1, a2):
    countmap = dict()
    next = dict()
    next[(a2[0], a2[1])] = 0
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
                if not isblocked(nx, ny) and (nx, ny) not in countmap and (nx, ny) not in temp:
                    temp[(nx,ny)] = counter
        next = temp
        steps = getSteps(countmap, a1)

    # if reachable
    if len(steps) != 0:
        return sorted(steps, key = lambda x : (x[1], x[0]))[0]
    else:
        return [None]

def move(a):
    global actors
    # best steps from enemies
    steps = [[na[0], na[1]] + closestStep(a, na) for na in actors if na[3] != a[3]]

    # only where step is possible
    steps = [s for s in steps if s[2] != None]

    # skip when none possible
    if len(steps) == 0:
        return

    # best move
    bestmove = sorted(steps, key = lambda x : (x[4], x[1], x[0]))[0]
    a[0] = bestmove[2]
    a[1] = bestmove[3]

def getInrange(a):
    global actors
    inrange = list()
    for dir in adjacent:
        nx = a[0] + dir[0]
        ny = a[1] + dir[1]
        ind = inmap(actors, nx, ny)
        if ind != None and actors[ind][3] != a[3]:
            inrange.append(ind)
    return inrange

def nextTick(tick):
    global actors
    actors = sorted(actors, key=lambda x: (x[1], x[0]), reverse=True)
    i = len(actors)-1

    while i >= 0:
        a = actors[i]
        inrange = getInrange(a) # get enemies in range
        if len(inrange) == 0:
            move(a)
            inrange = getInrange(a)

        if len(inrange) != 0:
            inrange = [actors[ai] + [ai] for ai in inrange]

            # lowest health in reading order
            cai = sorted(inrange, key = lambda x : (x[2], x[1], x[0]))[0][-1]

            # attack player
            actors[cai][2] -= a[5] # attack
            if actors[cai][2] <= 0:
                actors.pop(cai) # dead
                print("death -",cai)
                if minalive() == 0 and i != 0: # incomplete round
                    return False
                if cai < i: i -= 1

        if debug and False:
            print()
            print("small step -",a[4])
            drawMap()
            statusReport()
        i -= 1

    if debug:
        print()
        print("tick:", tick)
        drawMap()
        statusReport()
    else:
        print(tick)
    return True

def minalive():
    alive = [0,0]
    for a in actors:
        alive[1 * (a[3] == 0)] += 1
    return min(alive)

def sumHP():
    return sum(a[2] for a in actors)

def statusReport():
    global actors
    #drawMap()
    sactors = sorted(actors, key = lambda x:x[4])
    for a in sactors:
        print("HP:", a[2])
    print()

def elvesAlive():
    return len([a for a in actors if a[3] == 0])

def startBattle(eap):
    global actors
    setGame() # reset
    for a in actors:
        if a[3] == 0:
            a[5] = eap

    elfcount = elvesAlive()

    ticks = 0
    while minalive() > 0:
        if nextTick(ticks):
            ticks += 1
    statusReport()
    return ((sumHP() * ticks), (elfcount - elvesAlive())) # res and casualties

def solve1():
    res = startBattle(3)
    print("answer:", res[0]);

def solve2():
    eap = 4
    res = startBattle(eap)
    while res[1] != 0:
        eap += 1
        res = startBattle(eap)
    #print(eap)
    print("answer:",res[0])

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
