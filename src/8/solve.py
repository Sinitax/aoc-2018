from sys import argv as args

file = open("input.txt")
data = [int(x) for x in file.read().strip().split(" ")]
file.close()

#data = [int(x) for x in "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2".split(" ")]

def getNodes(nsize, index):
    nodes = list()
    for i in range(nsize):
        cnsize = data[index + 0]
        mdsize = data[index + 1]
        cnodes, index = getNodes(cnsize, index + 2)
        metadata = data[index:index + mdsize]
        nodes.append([cnodes, metadata])
        index = index + mdsize
    return nodes, index

def nodeSum(nodes):
    metadata = 0
    for n in nodes:
        metadata += sum(n[1]) + nodeSum(n[0])
    return metadata

def nodeValue(n):
    if len(n[0]) == 0:
        return sum(n[1])
    else:
        value = 0
        for i in range(len(n[1])):
            ni = n[1][i]-1
            if ni < len(n[0]):
                value += nodeValue(n[0][ni])
        return value

def solve1():
    nodes,index = getNodes(1, 0)
    print(nodeSum(nodes))

def solve2():
    nodes,index = getNodes(1, 0)
    print(nodeValue(nodes[0]))

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
