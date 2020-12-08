from sys import argv as args
from math import sqrt

def parseCommand(l):
    s = l.split(" ")
    args = [s[0]]
    args = args + [int(v) for v in s[1:]]
    return args

file = open("input.txt")
input = file.read()
file.close()

sinput = """#ip 0
seti 5 0 1
seti 6 0 2
addi 0 1 0
addr 1 2 3
setr 1 0 0
seti 8 0 4
seti 9 0 5"""

input = input.split("\n")

inspaddr = int(input[0][4:])

instructs = [parseCommand(l) for l in input[1:] if len(l) != 0]

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


def solve1():
    global register, insptr
    while register[inspaddr] < len(instructs):
        insptr = register[inspaddr]
        ins = instructs[insptr]
        #print(register)

        # execute command
        if len(register) <= ins[3]:
            register += [0 for x in range(ins[3] - len(register) + 1)]
        register[ins[3]] = opmap[ins[0]](ins[1], ins[2])

        # increment instruction pointer
        register[inspaddr] += 1

    print(register[0])


alpha = [chr(c + ord('a')) for c in range(26)]

dismap = dict()
dismap["addr"] = lambda a, b : "%s + %s" % (alpha[a], alpha[b])
dismap["addi"] = lambda a, b : "%s + %d" % (alpha[a], b)
dismap["mulr"] = lambda a, b : "%s * %s" % (alpha[a], alpha[b])
dismap["muli"] = lambda a, b : "%s * %d" % (alpha[a], b)
dismap["banr"] = lambda a, b : str(alpha[a] & alpha[b])
dismap["bani"] = lambda a, b : str(alpha[a] & b)
dismap["borr"] = lambda a, b : str(alpha[a] | alpha[b])
dismap["bori"] = lambda a, b : str(alpha[a] | b)
dismap["setr"] = lambda a, b : str(alpha[a])
dismap["seti"] = lambda a, b : str(a)
dismap["gtir"] = lambda a, b : "(%d > %s)" % (a, alpha[b])
dismap["gtri"] = lambda a, b : "(%s > %d)" % (alpha[a], b)
dismap["gtrr"] = lambda a, b : "(%s > %s)" % (alpha[a], alpha[b])
dismap["eqir"] = lambda a, b : "(%d == %s)" % (a, alpha[b])
dismap["eqri"] = lambda a, b : "(%s == %d)" % (alpha[a], b)
dismap["eqrr"] = lambda a, b : "(%s == %s)" % (alpha[a], alpha[b])

def disassemble():
    for i in range(len(instructs)):
        ins = instructs[i]
        print(i ,":",alpha[ins[3]],"=", dismap[ins[0]](ins[1], ins[2]))
    print()

def solve2(): # disassembled and reverse engineered to solve
    #disassemble()
    #return

    f = 10551276 # found by running

    res = 0
    sqrtf = sqrt(f)
    for i in range(1, int(sqrtf)):
        if f % i == 0:
            res += i + f / i

    if int(sqrtf) % f == 0:
        res += sqrtf

    print(int(res))
    """ divisor sum algo disassembled
    c = 1
    b = 1
    a = 0
    while b <= f:
        c = 1
        while c <= f:
            if b * c == f:
                a += b
            c += 1
        print(".")
        b += 1
    """

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
