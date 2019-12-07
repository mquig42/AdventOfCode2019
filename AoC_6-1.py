################################################################################
# AoC_6-1.py
# 2019-12-06
# Mike Quigley
#
# https://adventofcode.com/2019/day/6
#
# Reads a file where each line has two ID strings separated by a ')' char
# A)B means that B orbits A
# If C orbits B and B orbits A, then C indirectly orbits A
# Find the total number of direct and indirect orbits in the file
################################################################################

class Planet:
    def __init__(self, id):
        self.id = id
        self.children = []

    def orbitcount(self, depth):
        c = depth
        for child in self.children:
            c += child.orbitcount(depth + 1)
        return c

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

print(planetlist["COM"].orbitcount(0))
    
