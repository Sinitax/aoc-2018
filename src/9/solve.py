from collections import deque
from sys import argv as args

words = open("input.txt").read().split(" ")
playercount = int(words[0])
lastworth = int(words[6])

def getHighScore(playercount, lastworth): #optimized with deque
    lastworth = lastworth - lastworth % 23

    players = [0 for x in range(playercount)]
    marbles = deque([0])
    pos = 0
    for i in range(1, lastworth+1):
        if i % 23 == 0:
            cp = (i-1) % playercount
            players[cp] += i + marbles[(len(marbles) + pos - 7) % len(marbles)]
            marbles.rotate((len(marbles) - 1 - pos) + 7)
            marbles.pop()
            pos = 0
        else:
            if i < 3:
                pos = 1
                marbles.rotate(1)
                marbles.append(i)
            else:
                marbles.rotate((len(marbles)- 1 -pos) - 1)
                marbles.append(i)
                pos = len(marbles)-1
            #print(pos,marbles)

    print(max(players))


def solve1():
    getHighScore(playercount, lastworth)

def solve2():
    getHighScore(playercount, lastworth * 100)

def main():
    if len(args) > 1:
        if args[1] == "1":
            solve1()
        elif args[1] == "2":
            solve2()

main()
