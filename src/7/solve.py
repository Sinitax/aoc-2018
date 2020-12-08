from sys import argv as args

file = open("input.txt")
data = [x for x in file.readlines()]
file.close()

"""
data =
Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.
"""
#data = data.split("\n")

def removeReq(req, instructs): # remove requirements
    for res in instructs:
        if req in instructs[res]:
            instructs[res].remove(req)

def parseEntry(l):
    split = l.split(" ")
    firstl = split[1]
    nextl = split[-3]
    return firstl, nextl


def genInstructs():
    global data
    data = [parseEntry(l) for l in data if len(l) != 0]

    instructs = dict()

    for ins in data:
        req = ins[0]
        res = ins[1]
        if res not in instructs:
            instructs[res] = [ req ]
        else:
            instructs[res].append(req)

    values = list(instructs.values())[:]
    for reslist in values:
        for res in reslist:
            if res not in instructs:
                instructs[res] = []

    return instructs

def solve1():
    instructs = genInstructs()
    i = 0
    plan = list()
    while i < len(instructs):
        res = sorted(instructs.keys())[i] # alphabetically
        if len(instructs[res]) == 0:
            plan.append(res)
            instructs.pop(res, None)
            removeReq(res, instructs)
            i = 0
        else:
            i += 1

    print("".join(plan))

    return

def overlap(arr1, arr2):
    for a1 in arr1:
        if a1 in arr2:
            return True
    return False

def checkfail(workers):
    done = True
    for w in workers:
        if w[2]:
            done = False
            break
    return done

def solve2():
    instructs = genInstructs()
    # (5) worker: (task, time, done)
    workers = [["", 0, False] for x in range(5)]

    time = -1
    stop = False
    while not stop:
        time += 1
        for i in range(len(workers)):
            w = workers[i]
            if time >= w[1]:
                if w[2]:
                    removeReq(w[0], instructs)
                    #print("end : " + str(i) + " - " + str((w[0], w[1])))
                    w[2] = False
                    #i = 0
                    if len(instructs) == 0 and checkfail(workers):
                        stop = True
                        break

        for i in range(len(workers)):
            w = workers[i]
            if time >= w[1]:
                for res in sorted(instructs.keys()):
                    if len(instructs[res]) == 0:
                        w[0] = res
                        #print(instructs)
                        #print("start : " + str(i) + " - " + str((res, time)))
                        w[1] = time + ord(res)-65+1 + 60
                        w[2] = True
                        instructs.pop(res, None)
                        break

    #print()
    print(time)

    return

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
