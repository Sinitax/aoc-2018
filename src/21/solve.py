from sys import argv as args
from math import sqrt

def parseCommand(l):
    s = l.split(" ")
    args = [s[0]]
    args = args + [int(v) for v in s[1:]]
    return args

file = open("input.txt")
sinput = file.read()
file.close()

ainput = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""

sinput = sinput.split("\n")

inspaddr = int(sinput[0][4:])

instructs = [parseCommand(l) for l in sinput[1:] if len(l) != 0]

register = [0 for x in range(inspaddr+1)]

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

def varname(v):
    return "R"+str(v)

dismap = dict()
dismap["addr"] = lambda a, b : "%s + %s" % (varname(a), varname(b))
dismap["addi"] = lambda a, b : "%s + %d" % (varname(a), b)
dismap["mulr"] = lambda a, b : "%s * %s" % (varname(a), varname(b))
dismap["muli"] = lambda a, b : "%s * %d" % (varname(a), b)
dismap["banr"] = lambda a, b : "%s & %s" % (varname(a), varname(b))
dismap["bani"] = lambda a, b : "%s & %d" % (varname(a), b)
dismap["borr"] = lambda a, b : "%s | %s" % (varname(a), varname(b))
dismap["bori"] = lambda a, b : "%s | %d" % (varname(a), b)
dismap["setr"] = lambda a, b : "%s" % (varname(a))
dismap["seti"] = lambda a, b : "%d" % (a)
dismap["gtir"] = lambda a, b : "(%d > %s)" % (a, varname(b))
dismap["gtri"] = lambda a, b : "(%s > %d)" % (varname(a), b)
dismap["gtrr"] = lambda a, b : "(%s > %s)" % (varname(a), varname(b))
dismap["eqir"] = lambda a, b : "(%d == %s)" % (a, varname(b))
dismap["eqri"] = lambda a, b : "(%s == %d)" % (varname(a), b)
dismap["eqrr"] = lambda a, b : "(%s == %s)" % (varname(a), varname(b))

def disassemble(s, e):
    for i in range(s, e):
        ins = instructs[i]
        print(i ,":",varname(ins[3]),"=", dismap[ins[0]](ins[1], ins[2]))
    print()

def executeProgram():
    global register, insptr
    while register[inspaddr] < len(instructs):
        insptr = register[inspaddr]
        ins = instructs[insptr]

        # execute command
        if len(register) <= ins[3]:
            register += [0 for x in range(ins[3] - len(register) + 1)]
        register[ins[3]] = opmap[ins[0]](ins[1], ins[2])

        # part 1
        #if insptr == 13 and register[4] == 1:
        #    print(register)
        #    return

        # increment instruction pointer
        register[inspaddr] += 1

### SETUP


### PROGRAM CODE


def solve1():
    r0 = 1797184 # (first opportunity for comparison r1 and r0)

    #disassemble(0, len(instructs))
    #executeProgram()

    print(r0)
    return

def solve2():
    r1 = 0
    possibles = list()
    while True:
        r4 = r1 | 65536 # flip 9th bit
        r1 = 3798839
        while True: # scan bytes of r4 and add them to r1 and multiply
            r5 = r4 & 255
            r1 += r5
            r1 = r1 & 16777215
            r1 *= 65899  # equals 1 00000001 01101011
            r1 = r1 & 16777215
            if r4 < 256:
                break
            r4 = int(r4/256) # bit shift 8 to the right
        if r1 not in possibles:
            possibles.append(r1)
            #print("=>",r1)
        elif r1 == possibles[-1]:
            print(possibles[-1])
            break

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
