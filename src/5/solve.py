from sys import argv as args

file = open("input.txt")
input = file.read().strip()
file.close()

#s = list("dabAcCaCBAcCcaDA")


def reactPol(s):
    i = 0
    while i < len(s)-1:
        cs = "".join(s[i:i+2])
        csl = cs.lower()
        if csl[0] == csl[1] and cs[0] != cs[1]: # builds pair with next letter
            s.pop(i)
            s.pop(i) # pop both letters
            if i > 0:
                i -= 1 # check prev
        else:
            i += 1

    return len(s)

def solve1():
    print(reactPol(list(input)))

def solve2():
    min = None
    for i in range(26):
        ls = str(chr(i+97))
        print(f"\rTesting: {ls}", end="")
        cs = list(input.replace(ls, "").replace(ls.upper(), ""))
        len = reactPol(cs)
        if min == None or len < min:
            min = len
    print(f"\r            \r{min}")

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
