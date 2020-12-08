from sys import argv as args

file = open("input.txt")
data = [x for x in file.readlines()]
file.close()

#data = "#1 @ 1,3: 4x4","#2 @ 3,1: 4x4","#3 @ 5,5: 2x2"

def parserect(l):
    split = l.split("@")
    id = int(split[0].replace("#",""))
    split = split[1].split(":")
    pos = [int(x) for x in split[0].split(",")]
    size = [int(x) for x in split[1].split("x")]
    return pos, size, id

def createMap():
    global rectdata
    rectdata = [parserect(l) for l in data]
    msize = list([0,0])
    for i in range(len(rectdata)):
        r = rectdata[i]
        xm = r[0][0] + r[1][0]
        ym = r[0][1] + r[1][1]
        if i == 0 or xm > msize[0]:
            msize[0] = xm
        if i == 0 or ym > msize[1]:
            msize[1] = ym

    map = [[list() for y in range(msize[1])] for x in range(msize[0])]
    for r in rectdata:
        sx = r[0][0]
        sy = r[0][1]
        for x in range(sx, sx + r[1][0]):
            for y in range(sy, sy + r[1][1]):
                map[x][y].append(r[2])

    return map

def solve1(): # answer: 114946
    map = createMap()

    overlap = 0
    for x in range(len(map)):
        for y in range(len(map[0])):
            if len(map[x][y]) > 1:
                overlap += 1

    print(overlap)

def solve2(): # answer: 877
    map = createMap()

    overlap = set()
    for x in range(len(map)):
        for y in range(len(map[0])):
            if len(map[x][y]) > 1:
                for id in map[x][y]:
                    overlap.add(id)

    # print(overlap)

    for i in range(1, len(rectdata)):
        if i not in overlap:
            print(i)

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
