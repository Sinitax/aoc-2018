from sys import argv as args

lines = open("input.txt").read().split("\n")
istate = lines[0].split(": ")[1]
rules = [l.split(" => ") for l in lines[2:] if l != ""]
rules = [r[0] for r in rules if r[1] == "#"]

def nextGen(pots):
    pmin = min(pots)
    pmax = max(pots)
    npots = list()
    for i in range(pmin-4, pmax+1):
        for r in rules:
            match = True
            for j in range(5):
                if (r[j] == "#") != ((i+j) in pots):
                    match = False
                    break
            if match:
                npots.append(i+2)
                break
    return npots

def getPots():
    pots = list()
    for i in range(len(istate)):
        if istate[i] == "#":
            pots.append(i)
    return pots

def solve1():
    pots = getPots()
    for i in range(20):
        pots = nextGen(pots)
    print(sum(pots))
    return

def solve2():
    pots = getPots()
    psum = sum(pots)
    pdif = None
    i = 0
    while (True):
        pots = nextGen(pots)
        i += 1
        csum = sum(pots)
        if pdif == csum - psum:
            print(csum + pdif * (50000000000 - 164))
            break
        pdif = csum - psum
        psum = csum
    return

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
