from sys import argv as args

file = open("input.txt")
data = [x for x in file.readlines()]
file.close()

def parse_entry(l):
    split = l.split(" ")
    date = " ".join(split[:2])
    time = int(split[1].split(":")[1].replace("]",""))
    if split[2] == "Guard":
        awake = None
        id = int(split[3].replace("#",""))
    else:
        id = 0
        awake = (True if split[2] == "wakes" else False)
    return time, id, awake, date

class guard:
    def __init__(self, _id):
        self.shifts = list()
        self.id = _id
        self.awake = None

def gen_shiftmap():
    shiftdata = [parse_entry(l) for l in data]
    shiftdata = sorted(shiftdata, key=lambda x: x[3]) #sort by date

    shiftmap = dict()
    ltime = shiftdata[0][0]
    cgid = shiftdata[0][1]
    for i in range(len(shiftdata)):
        entry = shiftdata[i]
        ctime = entry[0]
        gid = entry[1]
        cawake = entry[2]

        if gid != 0: # new shift
            if gid not in shiftmap:
                shiftmap[gid] = guard(gid)
            #if i != 0 and not shiftmap[cgid].awake: # not first
            #    shiftmap[cgid].shifts.append((ltime, timedif(ctime, ltime), None))
            #ltime = ctime
            cgid = gid
        else:
            g = shiftmap[cgid]
            if cawake:
                if not g.awake:
                    shiftmap[cgid].shifts.append((ltime, ctime - ltime))
            else:
                ltime = ctime
            g.awake = cawake

    return shiftmap

def solve1():
    shiftmap = gen_shiftmap()

    maxsleep = None
    mg = None
    for g in shiftmap.values():
        minslept = 0
        for t in g.shifts:
            minslept += t[1]
        if not maxsleep or minslept > maxsleep:
            maxsleep = minslept
            mg = g


    timel = [0 for x in range(60)]

    for t in mg.shifts:
        for i in range(t[0], t[0] + t[1]):
            timel[(i-1)%60] += 1

    minute = timel.index(max(timel))+1
    print(minute * mg.id)

def solve2():
    shiftmap = gen_shiftmap()
    timetables = dict()

    for g in shiftmap.values():
        timetables[g.id] = [0 for x in range(60)]
        for t in g.shifts:
            for i in range(t[0], t[0] + t[1]):
                timetables[g.id][i] += 1

    max = None
    mmin = None
    mgid = None
    for i in range(60):
        for gid in timetables:
            t = timetables[gid]
            if max is None or t[i] > max:
                max = t[i]
                mmin = i
                mgid = gid

    print(mgid * mmin)

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
