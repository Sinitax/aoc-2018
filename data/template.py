from sys import argv as args

file = open("input.txt")
sinput = file.read() 
file.close()

def parseLine():
	return

sinput = [parseLine(l) for l in sinput.split("\n")]

def solve1():
	return

def solve2():
	return

def main():
	if len(args) > 1:
		if args[1] == "1":
			solve1()
		elif args[1] == "2":
			solve2()

main()
