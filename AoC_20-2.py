################################################################################
# AoC_20-2.py
# 2019-12-20
# Mike Quigley
#
# https://adventofcode.com/2019/day/20
#
# For part 2, the maze is recursive. Portals lead to another copy of the maze.
# The description on the website says that inner levels are smaller, but
# the numbers say that all levels are the same size
#
# Portals on the inner rim of the doughnut lead to an inner level, portals on
# the outer rim lead back out. You start at level 0, where outer portals are
# not traversable (Except for AA and ZZ)
#
# Find the length of the shortest route between AA and ZZ
################################################################################
import time

maze = []
portals = dict()

#Returns the 2 letter portal ID code located at the given coords
#Coords will not be at edge of map
def portalcode(x, y, maze):
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
def portalcoords(x, y, maze):
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
def map_portal(x, y, maze):
    if x == 0 or y == 0 or x == len(maze[0]) - 1 or y == len(maze) - 1:
        return
    coords = portalcoords(x, y, maze)
    if coords[0] == -1:
        return

    code = portalcode(x, y, maze)
    if code in portals:
        #Make coord linking entries in portals
        portals[coords] = portals[code]
        portals[portals[code]] = coords
    else:
        #Put this in portals
        portals[code] = coords

#Returns the contents of all asjacent spaces, including through a portal
#Outer portals have x or y coord == 2 or == len - 3
def adj(x, y, level):
    r = [maze[level][y-1][x],
         maze[level][y][x-1],
         maze[level][y+1][x],
         maze[level][y][x+1]]
    if (x, y) in portals:
        ll = linklevel(x, y, level)
        if ll > -1:
            coords = portals[(x, y)]
            r.append(maze[ll][coords[1]][coords[0]])
    return r

#Returns recursion level that the portal at given coords points to
#Or -1 if it's at the limit
def linklevel(x, y, level):
    if x==2 or y==2 or x==len(maze[0][0])-3 or y==len(maze[0])-3:
        #Outer portal, go up a level, or return -1 if level is 0
        return level - 1
    elif level == len(maze) - 1:
        #Inner portal at maximum recursion level. Return -1
        return -1
    else:
        #Inner portal. Go down a level
        return level + 1

#Finds distance between any 2 points in the maze
def distbetween(start, end):
    d = 0
    
    while True:
        for lev in range(len(maze)):
            for y in range(1, len(maze[0]) - 1):
                for x in range(1, len(maze[0][0]) - 1):
                    if maze[lev][y][x] != '.':
                        continue
                    if (x, y) == start:
                        maze[0][y][x] = '%'
                        continue

                    if '&' in adj(x, y, lev):
                        if (x, y) == end and lev == 0:
                            return d
                        maze[lev][y][x] = '%'

        flag = False                
        for lev in range(len(maze)):
            for y in range(len(maze[0])):
                for x in range(len(maze[0][0])):
                    if maze[lev][y][x] == '%':
                        maze[lev][y][x] = '&'
                        flag = True
        d += 1
        if not flag:
            #No solution found
            return -1

starttime = time.time()
file = open('AoC_20.txt','r')
toplayer = [list(line.strip('\n')) for line in file]
file.close()

for y in range(len(toplayer)):
    for x in range(len(toplayer[0])):
        if toplayer[y][x].isalpha():
            map_portal(x, y, toplayer)

for i in range(30):
    maze.append([y[:] for y in toplayer])

print(distbetween(portals['AA'], portals['ZZ']))
print('Elapsed time: {0:0.3f}s'.format(time.time() - starttime))

    
