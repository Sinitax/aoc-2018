from sys import argv as args

f = open("input.txt")
contents = f.read()
test_contents = """
/>-<\\
|   |
| /<+-\\
| | | v
\\>+</ |
  |   ^
  \\<->/
"""

tmap = [list(l) for l in contents.split("\n") if len(l) != 0]
xlen = len(tmap[0])
ylen = len(tmap)
f.close()

arrows = dict()
arrows["<"] = (-1, 0)
arrows[">"] = (1, 0)
arrows["^"] = (0, -1)
arrows["v"] = (0, 1)

directions = [(-1,0), (0,-1), (1, 0), (0, 1)] # l - u - r - d

def checkPos(x,y):
    if x < xlen and x >= 0 and y < ylen and y >= 0:
        return tmap[y][x]
    return " "

def correct(x, y):
    cr = checkPos(x+1, y)
    cl = checkPos(x-1, y)
    cu = checkPos(x, y-1)
    cd = checkPos(x, y+1)

    if cr == "|": cr = " "
    if cl == "|": cl = " "
    if cu == "-": cu = " "
    if cd == "-": cd = " "

    r = cr != " "
    l = cl != " "
    u = cu != " "
    d = cd != " "

    sum = r + l + u + d

    if sum > 2:
        return "+"

    # 2 around
    if r:
        if l:
            return "-"
        elif u:
            return "/"
        else:
            return "\\"
    else:
        if not l:
            return "|"
        elif u:
            return "/"
        else:
            return "\\"

carts = list()
for y in range(ylen):
    for x in range(xlen):
        if tmap[y][x] in arrows:
            carts.append([x, y, arrows[tmap[y][x]], 0, 0])
            tmap[y][x] = correct(x,y)

def cartAt(x, y):
    global carts
    for i in range(len(carts)):
        c = carts[i]
        if c[0] == x and c[1] == y and not c[4]:
            return i
    return None

def drawMap():
    for y in range(ylen):
        print("".join(["#" if cartAt(x,y) != None else tmap[y][x] for x in range(len(tmap[y]))]))

def advance(cart):
    ncart = [0 for x in range(5)]
    ncart[0] = cart[0]+cart[2][0]
    ncart[1] = cart[1]+cart[2][1]
    col = cartAt(ncart[0], ncart[1])
    if col != None:
        return ncart[0], ncart[1], col

    c = tmap[ncart[1]][ncart[0]]
    d = directions.index(cart[2])

    if c == "+":
        d = (d + len(directions)-1 + cart[3]) % len(directions)
        ncart[2] = directions[d]
        ncart[3] = (cart[3] + 1) % 3
    else: #dont need to change direction for '-' and '|'
        if c == "/":
            ncart[2] = directions[3-d]
        elif c == "\\":
            if d == 0: #l
                ncart[2] = directions[1]
            elif d == 1: #u
                ncart[2] = directions[0]
            elif d == 2: #r
                ncart[2] = directions[3]
            elif d == 3: #d
                ncart[2] = directions[2]
        else:
            ncart[2] = cart[2]
        ncart[3] = cart[3]
    return ncart


def solve1():
    global carts

    crash = None
    while not crash:
        carts = sorted(carts, key=lambda x:(x[0], x[1]))
        for c in range(len(carts)):
            nc = advance(carts[c])
            if len(nc) == 3:
                crash = nc
                break
            else:
                carts[c] = nc

    print(f"{crash[0]},{crash[1]}")

def solve2():
    global carts

    while len(carts) > 1:
        carts = sorted(carts, key=lambda x:(x[0], x[1]))
        rcarts = list()
        for c in range(len(carts)):
            if carts[c][4]: continue;
            nc = advance(carts[c])
            if len(nc) == 3:
                carts[c][4] = 1
                carts[nc[2]][4] = 1
                rcarts.append(carts[c])
                rcarts.append(carts[nc[2]])
            else:
                carts[c] = nc
        for c in rcarts:
            if c in carts: # prevent doubles
                carts.remove(c)

    print(f"{carts[0][0]},{carts[0][1]}")

def main():
    if len(args) == 2:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
