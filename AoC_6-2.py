################################################################################
# AoC_6-2.py
# 2019-12-06
# Mike Quigley
#
# https://adventofcode.com/2019/day/6#part2
#
# Using same orbit file as part 1, find number of transfers required to
# travel from parent planet of YOU to parent planet of SAN
################################################################################

class Planet:
    def __init__(self, id):
        self.id = id
        self.parent = None
        self.children = []

    def pathto(self):
        path = []
        if not self.parent == None:
            path = self.parent.pathto()
        path.append(self.id)
        return path
        

file = open("AoC_6-1.txt","r")
planetlist = dict()

for line in file:
    rec = line.strip().split(')')
    if rec[0] in planetlist:
        parent = planetlist[rec[0]]
    else:
        parent = Planet(rec[0])
        planetlist[rec[0]] = parent
    if rec[1] in planetlist:
        child = planetlist[rec[1]]
    else:
        child = Planet(rec[1])
        planetlist[rec[1]] = child
    parent.children.append(child)
    child.parent = parent

path2u = planetlist["YOU"].pathto()
path2s = planetlist["SAN"].pathto()
i = 0
while path2u[i] == path2s[i]:
    i += 1

print(len(path2u) + len(path2s) - 2*i - 2)
    
