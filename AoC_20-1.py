################################################################################
# AoC_20-1.py
# 2019-12-20
# Mike Quigley
#
# https://adventofcode.com/2019/day/20
#
# Another maze challenge, this time with portals          A
# Each portal is a 2 letter code, written as either AB or B
# Each portal code appears exactly twice, and the two are linked
# Except for AA and ZZ which only appear once
#
# Find the length of the shortest route between AA and ZZ
################################################################################

maze = []
portals = dict()

#Returns the 2 letter portal ID code located at the given coords
#Coords will not be at edge of map
def portalcode(x, y):
    if maze[y-1][x].isalpha():
        return ''.join([maze[y-1][x], maze[y][x]])
    if maze[y+1][x].isalpha():
        return ''.join([maze[y][x], maze[y+1][x]])
    if maze[y][x-1].isalpha():
        return ''.join([maze[y][x-1], maze[y][x]])
    if maze[y][x+1].isalpha():
        return ''.join([maze[y][x], maze[y][x+1]])
    return ''

#Returns coords of any '.' space adjacent to given coords
#If there are no adjacent '.'s, return (-1, -1)
def portalcoords(x, y):
    if maze[y-1][x] == '.':
        return (x, y-1)
    if maze[y+1][x] == '.':
        return (x, y+1)
    if maze[y][x-1] == '.':
        return (x-1, y)
    if maze[y][x+1] == '.':
        return (x+1, y)
    return (-1, -1)

#If this portal ID hasn't been seen before, store coords of adjacent '.' space
#in portals dict with portal ID as key
#If it has been seen before, create 2 dict entries linking the coords of the
#2 portals.
#If coords are not adjacent to a '.' space, do nothing
def map_portal(x, y):
    if x == 0 or y == 0 or x == len(maze[0]) - 1 or y == len(maze) - 1:
        return
    coords = portalcoords(x, y)
    if coords[0] == -1:
        return

    code = portalcode(x, y)
    if code in portals:
        #Make coord linking entries in portals
        portals[coords] = portals[code]
        portals[portals[code]] = coords
    else:
        #Put this in portals
        portals[code] = coords

#Returns the contents of all asjacent spaces, including through a portal
def adj(x, y):
    r = [maze[y-1][x],maze[y][x-1],maze[y+1][x],maze[y][x+1]]
    if (x, y) in portals:
        coords = portals[(x, y)]
        r.append(maze[coords[1]][coords[0]])
    return r

#Finds distance between any 2 points in the maze
def distbetween(start, end):
    d = 0
    
    while True:
        for y in range(1, len(maze) - 1):
            for x in range(1, len(maze[0]) - 1):
                if maze[y][x] != '.':
                    continue
                if (x, y) == start:
                    maze[y][x] = '%'
                    continue

                if '&' in adj(x, y):
                    if (x, y) == end:
                        return d
                    maze[y][x] = '%'
                
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if maze[y][x] == '%':
                    maze[y][x] = '&'
        d += 1

file = open('AoC_20.txt','r')
maze = [list(line.strip('\n')) for line in file]
file.close()

for y in range(len(maze)):
    for x in range(len(maze[0])):
        if maze[y][x].isalpha():
            map_portal(x, y)

print(distbetween(portals['AA'], portals['ZZ']))

    
