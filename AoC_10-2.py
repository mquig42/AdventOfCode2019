################################################################################
# AoC_10-2.py
# 2019-12-10
# Mike Quigley
#
# https://adventofcode.com/2019/day/10#part2
#
# Part 1 has chosen the coords (20,19) for the asteroid monitoring station
# 284 asteroids are visible from this point
# If a giant laser sweeps around clockwise from 12:00,
# find the coords of the 200th asteroid to be vaporized
#
# I got lucky with the input here. This program wouldn't work if fewer than
# 200 asteroids were visible. If that were the case, I would have to deal with
# removing asteroids to see what's behind them
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

#Finds the distance between 2 asteroids
def distance(ass1, ass2):
    a = abs(ass1[0] - ass2[0])
    b = abs(ass1[1] - ass2[1])
    return math.sqrt(a*a + b*b)

#Makes a list of visible asteroids
def listeroids(ass):
    visteroids = dict()
    for oth in asteroids:
        if ass != oth:
            ang = angle(ass[0],ass[1],oth[0],oth[1])
            if ang in visteroids:
                if distance(ass, oth) < distance(ass, visteroids[ang]):
                    visteroids[ang] = oth
            else:
                visteroids[ang] = oth
    return visteroids

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
            
visteroids = listeroids((20,19))
orderoids = sorted(list(visteroids))

for i in range(len(orderoids)):
    print(i+1, ":", visteroids[orderoids[i]])

print(visteroids[orderoids[200-1]])

