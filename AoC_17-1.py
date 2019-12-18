################################################################################
# AoC_17-1.py
# 2019-12-17
# Mike Quigley
#
# https://adventofcode.com/2019/day/17
#
# The ASCII Intcode program will produce a stream of integers representing
# ASCII characters. Display the resulting ASCII art, then find the coords
# of any scaffold intersections and calculate a checksum
################################################################################
import INTCODE_T

def is_intersect(x, y, ls):
    #Intersections don't happen on the edge
    if x == 0 or y == 0 or x == len(ls[0]) - 1 or y == len(ls) - 1:
        return False
    #Must be a scaffold
    if ls[y][x]=='.':
        return False
    #Look at adjacent squares
    if ls[y][x-1]=='.' or ls[y][x+1]=='.' or ls[y-1][x]=='.' or ls[y+1][x]=='.':
        return False
    return True

asci = INTCODE_T.Intcomp_T(1, 'asci', 4096)
asci.loadfile('ASCII')
asci.start()

rawview = []
c = asci.outQ.get()
while c != 'END':
    rawview.append(chr(c))
    c = asci.outQ.get()

lines = ''.join(rawview).split('\n')
lines = lines[:lines.index('')]

chk = 0
for y in range(len(lines)):
    for x in range(len(lines[0])):
        if is_intersect(x, y, lines):
            templine = list(lines[y])
            templine[x] = 'O'
            lines[y] = ''.join(templine)
            chk += x*y

for line in lines:
    print(line)

print(chk)

