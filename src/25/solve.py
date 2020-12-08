from sys import argv as args

sinput = open("input.txt").read()

ainput = """1,-1,-1,-2
-2,-2,0,1
0,2,1,3
-2,3,-2,1
0,2,3,-2
-1,-1,1,-2
0,-2,-1,0
-2,2,3,-1
1,2,2,0
-1,-2,0,-2"""

ainput = """1,-1,0,1
2,0,-1,0
3,2,-1,0
0,0,3,1
0,0,-1,-1
2,3,-2,0
-2,2,0,0
2,-2,0,-1
1,-1,0,-1
3,2,0,2"""

ainput = """0,0,0,0
 3,0,0,0
 0,3,0,0
 0,0,3,0
 0,0,0,3
 0,0,0,6
 9,0,0,0
12,0,0,0"""

ainput = """-1,2,2,0
0,0,2,-2
0,0,0,-2
-1,2,0,0
-2,-2,-2,2
3,0,2,-1
-1,3,2,2
-1,0,-1,0
0,2,1,-2
3,0,0,0"""

def parseLine(l):
    return [int(v) for v in l.split(",")]

coordinates = [parseLine(l) for l in sinput.split("\n") if len(l) != 0]

def dist(c1, c2):
    return sum([abs(c1[i] - c2[i]) for i in range(4)])

def getClose(coords, c):
    match = list()
    j = 0
    while j in range(len(coords)):
        if dist(c, coords[j]) <= 3:
            match.append(coords[j])
            coords.pop(j)
        else:
            j += 1
    return match

def solve1():
    constellations = list()
    available = coordinates[:]

    while len(available) != 0:
        match = getClose(available, available[0])

        j = 0
        while j < len(match):
            match += getClose(available, match[j])
            j += 1

        constellations.append(match)

    print(len(constellations))

    """
    sum = 0
    for cons in constellations:
        sum += len(cons)
    print(sum)
    """
    return

def solve2():
    return

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
