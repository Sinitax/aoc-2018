from sys import argv as args


def parseLog(ls):
    data = list()
    before = [int(v) for v in ls[0].split("[")[1].split("]")[0].split(",")]
    ins = [int(v) for v in ls[1].split(" ")]
    after = [int(v) for v in ls[2].split("[")[1].split("]")[0].split(",")]
    return (before, ins, after)

file = open("input.txt")
inslog = list()
input = file.readlines()
file.close()
progsec = None

for i in range(0, len(input), 4):
    if input[i] == "\n":
        progsec = i
        break
    inslog.append(parseLog(input[i:i+4]))


register = list()

opmap = dict()
opmap["addr"] = lambda a, b : register[a] + register[b]
opmap["addi"] = lambda a, b : register[a] + b
opmap["mulr"] = lambda a, b : register[a] * register[b]
opmap["muli"] = lambda a, b : register[a] * b
opmap["banr"] = lambda a, b : register[a] & register[b]
opmap["bani"] = lambda a, b : register[a] & b
opmap["borr"] = lambda a, b : register[a] | register[b]
opmap["bori"] = lambda a, b : register[a] | b
opmap["setr"] = lambda a, b : register[a]
opmap["seti"] = lambda a, b : a
opmap["gtir"] = lambda a, b : 1 * (a > register[b])
opmap["gtri"] = lambda a, b : 1 * (register[a] > b)
opmap["gtrr"] = lambda a, b : 1 * (register[a] > register[b])
opmap["eqir"] = lambda a, b : 1 * (a == register[b])
opmap["eqri"] = lambda a, b : 1 * (register[a] == b)
opmap["eqrr"] = lambda a, b : 1 * (register[a] == register[b])

def getPossible(ins):
    global register
    sregister = register[:]
    before = ins[0]
    after = ins[2]
    register = before
    a = ins[1][1]
    b = ins[1][2]
    c = ins[1][3]
    ops = list(opmap.values())
    possibles = list()
    for i in range(len(ops)):
        op = ops[i]
        res = None
        try:
            res = op(a, b)
        except:
            continue
        if res == after[c]:
            possibles.append(i)
    register = sregister
    return possibles

def solve1():
    global register
    uncertain = 0
    for ins in inslog:
        if len(getPossible(ins)) >= 3:
            uncertain += 1
    print(uncertain)
    return

def solve2():
    possible = dict()
    for ins in inslog:
        o = ins[1][0]
        if o in possible:
            possible[o] = [op for op in getPossible(ins) if op in possible[o]]
        else:
            possible[o] = getPossible(ins)

    certain = False
    while not certain:
        singles = [p[0] for p in possible.values() if len(p) == 1]
        for p in possible:
            if len(possible[p]) != 1:
                possible[p] = [v for v in possible[p] if v not in singles]

        certain = True
        for p in possible.values():
            if len(p) != 1:
                certain = False
                break

    ntrans = dict()
    for p in possible: # flatten
        ntrans[p] = possible[p][0]

    for i in range(progsec, len(input)): # execute program
        l = input[i]
        if l == "\n": continue
        cmd = [int(v) for v in l.split(" ")]
        while len(register)-1 < cmd[3]:
            register.append(0)

        register[cmd[3]] = list(opmap.values())[ntrans[cmd[0]]](cmd[1], cmd[2])


    print(register[0])

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
