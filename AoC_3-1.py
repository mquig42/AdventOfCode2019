################################################################################
# AoC_3-1.py
# 2019-12-04
# Mike Quigley
#
# https://adventofcode.com/2019/day/3
#
# Given two paths through a grid, finds the closest intersection
# based on Manhattan distance (See Wikipedia article on taxicab geometry)
################################################################################

def coords(path):
    x = 0
    y = 0
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
            detailedPath.append((x,y))
    return detailedPath

inp = open("AoC_3-1.txt","r")
path1 = inp.readline()
path2 = inp.readline()
inp.close()

coords1 = coords(path1)
coords2 = coords(path2)

minDist = 999999
minInt = (0,0)

for i in list(set(coords1)&set(coords2)):
    dist = abs(i[0]) + abs(i[1])
    if dist < minDist:
        minDist = dist
        minInt = i

print(minInt, minDist)
