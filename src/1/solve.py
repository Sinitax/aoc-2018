from sys import argv as args

file = open("input.txt")
data = [int(x) for x in file.readlines()]
file.close()

def solve1(): # answer: 411
    print(sum(data))

def solve2(): # answer: 56360
    totshift = 0
    fvals = list()
    for c in data:
        fvals.append(totshift)
        totshift += c
    print("total shift: " + str(totshift))

    doubles = list()

    if totshift == 0:
        doubles.append([len(data), 0])

    i = 0
    while i < len(fvals):
        for j in range(len(fvals)):
            if i == j:
                continue
            dif = fvals[j] - fvals[i]
            if dif % totshift == 0:
                inds = list([i, j])
                if j > i:
                    inds = inds[::-1]
                if totshift > 0: #ends on c
                    if fvals[inds[0]] > fvals[inds[1]]:
                        inds = inds[::-1]
                else:
                    if fvals[inds[0]] < fvals[inds[1]]:
                        inds = inds[::-1]

                pos = (abs(dif) // totshift) * len(data) + inds[0]
                doubles.append([pos, fvals[inds[1]]])
        i += 1

    if len(doubles) == 0: #fail
        return

    min = doubles[0]
    for d in doubles:
        if d[0] < min[0]:
            min = d

    print(min[1])

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
