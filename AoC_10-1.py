################################################################################
# AoC_10-1.py
# 2019-12-10
# Mike Quigley
#
# https://adventofcode.com/2019/day/10
#
# Input is a grid where each square contains . for empty or # for asteroid
# Find the coordinates of the asteroid with line of sight to as many
# other asteroids as possible. Lines can be at any angle. An asteroid blocks
# LoS to any other asteroids behind it.
################################################################################
import math

grid = []
asteroids = []
minX = 0
minY = 0
maxX = 0
maxY = 0

#Quadrants:
# D | A
# --+--
# C | B
#Returns angle measured from 12:00 in radians
def angle(x0,y0,x1,y1):
    if x0 == x1:
        #Vertical line
        return 0 if y0 > y1 else math.pi
    elif y0 == y1:
        #Horizontal line
        return 0.5 * math.pi if x0 < x1 else 1.5 * math.pi
    elif x0 < x1 and y0 > y1:
        #Quadrant A
        return math.atan((x1 - x0) / (y0 - y1))
    elif x0 < x1 and y0 < y1:
        #Quadrant B
        return math.pi - math.atan((x1 - x0) / (y1 - y0))
    elif x0 > x1 and y0 < y1:
        #Quadrant C
        return math.pi + math.atan((x0 - x1) / (y1 - y0))
    elif x0 > x1 and y0 > y1:
        #Quadrant D
        return 2 * math.pi - math.atan((x0 - x1) / (y0 - y1))

#Returns number of other asteroids visible from ass
def viscount(ass):
    angles = dict()
    for oth in asteroids:
        if ass != oth:
            angles[angle(ass[0],ass[1],oth[0],oth[1])] = oth
    return len(angles)

#Read input
file = open("AoC_10-1.txt","r")
grid = [line.strip() for line in file]
file.close()
maxX = len(grid[0]) - 1
maxY = len(grid) - 1

for line in grid:
    print(line)

#Make a list of all asteroids
for x in range(maxX + 1):
    for y in range(maxY + 1):
        if grid[y][x] == '#':
            asteroids.append((x, y))

maxvis = 0
for ass in asteroids:
    vc = viscount(ass)
    if vc > maxvis:
        print(ass, vc)
        maxvis = vc
