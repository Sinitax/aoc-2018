from sys import argv as args

inputstr = open("input.txt").read().replace("\n","")
recipes = [3,7]

def solve1():
    global recipes, inputstr

    end = int(inputstr)
    workers = [i for i in range(2)]
    while len(recipes) < end + 10:
        recipes += [int(c) for c in str(sum(recipes[workers[i]] for i in range(len(workers))))]
        for i in range(len(workers)):
            workers[i] = (workers[i] + recipes[workers[i]]+1) % len(recipes)
    print("".join([str(x) for x in recipes[end:]]))

def solve2():
    global recipes, inputstr

    ilen = len(inputstr)
    inputstr = [int(c) for c in inputstr]
    workers = [i for i in range(2)]
    stop = False
    counter = 0
    while not stop:
        for v in [int(c) for c in str(sum(recipes[workers[i]] for i in range(len(workers))))]:
            if recipes[-ilen:] == inputstr:
                stop = True
                break
            recipes.append(v)
        for i in range(len(workers)):
            workers[i] = (workers[i] + recipes[workers[i]]+1) % len(recipes)
    print(len(recipes)-ilen)

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
