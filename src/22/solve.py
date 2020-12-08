# second part was solved with help from subreddit

from sys import argv as args
import networkx

adjacent = [[-1, 0], [0, -1], [1, 0], [0, 1]]

# load file
file = open("input.txt")
sinput = file.read()
file.close()

# create symbol definitions
symbols = [".", "=", "|"]
rocky, wet, narrow = 0, 1, 2
torch, gear, neither = 0, 1, 2

tooloptions = dict()
tooloptions[rocky] = (torch, gear)
tooloptions[wet] = (gear, neither)
tooloptions[narrow] = (torch, neither)

# parse input file
def parseInput(si):
    s = si.split("\n")
    depth = int(s[0].split(": ")[1])
    target = [int(v) for v in s[1].split(": ")[1].split(",")]
    return depth, target

# get erosion level from geological index
def getErosionLevel(n):
    return (n + depth) % 20183

# generate map of erosion types
def genMap():
    grid = [[0 for x in range(mrange[0])] for y in range(mrange[1])]

    # generate values on x side
    grid[0] = [getErosionLevel(x * 16807) for x in range(mrange[0])] 

    # generate values on y side
    for y in range(mrange[1]):
        grid[y][0] = getErosionLevel(y * 48271)

    # fill in other positions
    for y in range(1, mrange[1]):
        for x in range(1, mrange[0]):
            grid[y][x] = getErosionLevel(grid[y-1][x] * grid[y][x-1])

    # mod 3 for env type
    grid = [[grid[y][x] % 3 for x in range(mrange[0])] for y in range(mrange[1])]

    # start position is rocky
    grid[target[1]][target[0]] = 0

    return grid

# define constants from input file
depth, target = parseInput(sinput)
mrange = (target[0] + 100, target[1] + 100) # 100 block padding for potential hook-paths

vmap = genMap()

# risk level of area is sum of risk levels
def getRiskLevel(width, height):
    risk = 0
    for y in range(height + 1):
        for x in range(width + 1):
            risk += vmap[y][x]
    return risk


# indices of blocks around pos p
def getAround(p):
    return [[p[0] + di[0], p[1] + di[1]] for di in adjacent]

# traverse grid using dijkstra's algorithm (3d)
def dijkstra():
    graph = networkx.Graph()
    for y in range(mrange[1]):
        for x in range(mrange[0]):
            tools = tooloptions[vmap[y][x]]
            graph.add_edge((x, y, tools[0]), (x, y, tools[1]), weight = 7) # always takes 7 minutes to switch, 2 z-options for each tool
            for (nx, ny) in getAround((x, y)): # for all surrounding positions
                if 0 <= nx < mrange[0] and 0 <= ny < mrange[1]:
                    ntools = tooloptions[vmap[ny][nx]]
                    for tool in [t for t in tools if t in ntools]: # if tool is usable in both environments
                        graph.add_edge((x, y, tool), (nx, ny, tool), weight = 1) # then it only takes 1 minute
    return networkx.dijkstra_path_length(graph, (0, 0, torch), (target[0], target[1], torch))

#print("setup done..")

### PROGRAM CODE

def solve1():
    print(getRiskLevel(target[0], target[1]))

def solve2():
    print(dijkstra())

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
