import sys
args = sys.argv

gridserial = int(open("input.txt").read())

# rack ID = x + 10
# intial power = rackID * y
# power += gridserial
# power *= rackID
# power = str(power)[2]
# power -= 5

def getPower(x,y):
    id = x + 10
    power = id * y
    power += gridserial
    power *= id
    spower = str(power)
    if len(spower) > 2:
        power = int(spower[-3])
    else:
        power = 0
    power -= 5
    return power

def solve1():
    maxpower = None
    coords = None
    for x in range(300-2):
        for y in range(300-2):
            power = 0;
            for i in range(3):
                for j in range(3):
                    power += getPower(x+i,y+j)
            if maxpower == None or power > maxpower:
                maxpower = power
                coords = (x, y)
    print(f"{coords[0]},{coords[1]}")

def genMap():
    vmap = [[0 for y in range(300)] for x in range(300)]
    for x in range(300):
        for y in range(300):
            vmap[x][y] = getPower(x,y)
    return vmap

def solve2():
    maxpower = None
    res = None
    pmap = genMap()
    vmap = [[list() for y in range(300)] for x in range(300)]
    for s in range(1, 301):
        print(f"\rTrying: {s}", end="")
        cmaxpower = None
        cres = None
        for x in range(300-(s-1)):
            for y in range(300-(s-1)):
                vmap[x][y] += [pmap[x+(s-1)][y+i] for i in range(s)]
                vmap[x][y] += [pmap[x+i][y+(s-1)] for i in range(s-1)]
                power = sum(vmap[x][y]);
                if cmaxpower == None or power > cmaxpower:
                    cmaxpower = power
                    cres = (x, y, s)
        if maxpower == None or cmaxpower > maxpower:
            maxpower = cmaxpower
            res = cres
        elif cmaxpower < maxpower:
            break

    print("\r" + " " * 50 + "\r", end="")
    print(f"{res[0]},{res[1]},{res[2]}")

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
