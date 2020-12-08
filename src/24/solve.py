from sys import argv as args

sinput = open("input.txt").read()

immunesys = 0
infection = 1
ctype = 0

# parse input from file
def parseInput():
    groups = list()
    for l in sinput.split("\n"):
        pl = parseLine(l)
        if pl != None:
            groups.append(pl)
    return groups

# parse line of input
def parseLine(line):
    global ctype
    group = None
    if "Immune" in line:
        ctype = immunesys
    elif "Infection" in line:
        ctype = infection
    elif line != "":
        ls = line.split()
        group = dict()
        group["type"] = ctype
        group["units"] = int(ls[0])
        group["unithp"] = int(ls[4])
        group["initiative"] = int(ls[-1])
        group["weak"] = list()
        group["immune"] = list()
        if "(" in line:
            parenthstr = line.split("(")[1].split(")")[0]
            traits = parenthstr.split(";")
            for traitstr in traits:
                info = traitstr.split()
                group[info[0]] = [v.replace(",","") for v in info[2:]]
        dmginfo = line.split("does")[1].split("damage")[0].split()
        group["dmg"] = int(dmginfo[0])
        group["dmgtype"] = dmginfo[1]
    return group

def getEffectivePower(g):
    return g["units"] * g["dmg"]

def getDamage(attacker, defender):
    dmg = getEffectivePower(attacker)
    dmg *= (0 if attacker["dmgtype"] in defender["immune"] else 1)
    dmg *= (2 if attacker["dmgtype"] in defender["weak"] else 1)
    return dmg

groups = parseInput()

def fight():
    global groups

    lunits = 0

    immalive = len([g for g in groups if g["type"] == immunesys])
    infalive = len([g for g in groups if g["type"] == infection])

    while immalive > 0 and infalive > 0:
        # target selection
        attacked = list()
        attackpairs = list()
        groups = sorted(groups, key = lambda x : (getEffectivePower(x), x["initiative"]), reverse = True)
        for group in groups:
            # choose group of other army, which is not already being attacked and sort appropriately
            enemies = [g for g in groups if g["type"] != group["type"] and g not in attacked]
            if len(enemies) == 0:
                continue
            target = max(enemies, key = lambda x : (getDamage(group, x), getEffectivePower(x), x["initiative"]))
            if getDamage(group, target) != 0: # enemies which arent immune
                attacked.append(target)
                attackpairs.append((groups.index(group), groups.index(target)))

        # attacking phase
        attackpairs = sorted(attackpairs, key = lambda x : groups[x[0]]["initiative"], reverse = True)

        for ap in attackpairs:
            attacker = groups[ap[0]]
            attacked = groups[ap[1]]
            if attacker["units"] > 0 and attacked["units"] > 0: # if attacker or defender is dead, no need to attack
                dmg = getDamage(attacker, attacked)
                attacked["units"] = max(0, attacked["units"] - dmg // attacked["unithp"]) # remove whole numbers of units

        groups = [g for g in groups if g["units"] > 0]
        immalive = sum([g["units"] for g in groups if g["type"] == immunesys])
        infalive = sum([g["units"] for g in groups if g["type"] == infection])
        units = immalive + infalive
        if units == lunits:
            return units
        lunits = units
    return units

def solve1():
    print(fight())

def solve2():
    global groups

    immunewin = False
    boost = 1
    while not immunewin:
        groups = parseInput()
        for g in groups:
            if g["type"] == immunesys:
                g["dmg"] += boost

        fight()

        immunewin = (sum([0 if g["type"] == immunesys else 1 for g in groups]) == 0)

        boost += 1

    #print("boost:", boost)
    print("units:", sum([v["units"] for v in groups]))

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
