################################################################################
# AoC_3-2.py
# 2019-12-04
# Mike Quigley
#
# https://adventofcode.com/2019/day/3#part2
#
# Given two paths through a grid, finds the closest intersection
# based on minimum step count
################################################################################

def coords(path):
    x = 0
    y = 0
    steps = 0
    sDict = dict()
    detailedPath = []
    for s in path.split(","):
        for n in range(int(s[1:])):
            if s[0] == 'L':
                x -= 1
            elif s[0] == 'R':
                x += 1
            elif s[0] == 'U':
                y += 1
            elif s[0] == 'D':
                y -= 1
            steps += 1
            detailedPath.append((x,y))
            if (x,y) not in sDict.keys():
                sDict[(x,y)] = steps
    return detailedPath, sDict

inp = open("AoC_3-1.txt","r")
path1 = inp.readline()
path2 = inp.readline()
inp.close()

coords1, steps1 = coords(path1)
coords2, steps2 = coords(path2)

minDist = 999999
minInt = (0,0)

for i in list(set(coords1)&set(coords2)):
    dist = steps1[i] + steps2[i]
    if dist < minDist:
        minDist = dist
        minInt = i

print(minInt, minDist)
