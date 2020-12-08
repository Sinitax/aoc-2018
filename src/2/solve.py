from sys import argv as args

file = open("input.txt")
data = [x.replace("\n","") for x in file.readlines()]
file.close()

def solve1():
    doubles = 0
    triples = 0
    for s in data:
        counts = list((0,) * 26) # characters
        for c in s:
            counts[ord(c[0])-97] += 1
        if 2 in counts:
            doubles += 1
        if 3 in counts:
            triples += 1
    print(doubles * triples)

def compare(s1, s2):
    dif = 0
    same = list()
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            dif += 1
        else:
            same.append(s1[i])
    return(dif, same)

def solve2():
    for i in range(len(data)):
        for j in range(i, len(data)):
            if i == j:
                continue
            res = compare(data[i], data[j])
            if res[0] == 1:
                print("".join(res[1]))
                return

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
