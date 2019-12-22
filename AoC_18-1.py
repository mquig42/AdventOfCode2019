################################################################################
# AoC_18-1.py
# 2019-12-18
# Mike Quigley
#
# https://adventofcode.com/2019/day/18
#
# Today's input is a large maze containing lowercase letters (keys) and
# uppercase letters (doors). Key a opens door A. Find the shortest path
# that collects every key.
#
# Some doors have no keys behind them, and can be regarded as dead ends.
# The filldeadends function can help find them, then continue filling in every
# dead end to make the maze easier to deal with.
#
# The deaddoors list is the only part of the program tailored to my specific
# input. Everything else is fully automatic.
# The program takes 55 minutes to run. I'm only using 1 CPU core, so some
# multithreading could speed that up.
################################################################################
import time

deaddoors = ['D','I','L','M','O','Q','S','U','W','Z']

distcache = dict()
availcache = dict()
remaincache = dict()

def readmaze(filename):
    maze = []
    file = open(filename,'r')
    for line in file:
        maze.append(list(line.strip()))
    file.close()
    return maze

def printmaze(maze):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            print('█' if maze[y][x] == '#' else maze[y][x],end='')
        print()

def isdeadend(x, y, maze):
    if maze[y][x] != '.' and maze[y][x] not in deaddoors:
        return False
    count = 0
    if maze[y][x+1] != '#':
        count += 1
    if maze[y][x-1] != '#':
        count += 1
    if maze[y+1][x] != '#':
        count += 1
    if maze[y-1][x] != '#':
        count += 1
    return count == 1

def filldeadends(maze):
    done = False
    while not done:
        done = True
        for y in range(len(maze)):
            for x in range(len(maze[0])):
                if isdeadend(x, y, maze):
                    maze[y][x] = '#'
                    done = False

def adjacent_squares(x, y, maze):
    return [maze[y][x-1],
            maze[y+1][x],
            maze[y][x+1],
            maze[y-1][x]]

#Finds distance between any 2 unique chars in the maze
def distbetween(start, end, maze):
    if (start, end) in distcache:
        return distcache[(start,end)]
    #Local copy
    tempmaze = [y[:] for y in maze]
    d = 0
    
    while True:
        for y in range(1, len(tempmaze) - 1):
            for x in range(1, len(tempmaze[0]) - 1):
                if tempmaze[y][x] == '#' or tempmaze[y][x] == '&':
                    continue
                if tempmaze[y][x] == start:
                    tempmaze[y][x] = '%'
                    continue

                if '&' in adjacent_squares(x, y, tempmaze):
                    if tempmaze[y][x] == end:
                        distcache[(start,end)] = d
                        return d
                    tempmaze[y][x] = '%'
                
        for y in range(len(tempmaze)):
            for x in range(len(tempmaze[0])):
                if tempmaze[y][x] == '%':
                    tempmaze[y][x] = '&'
        d += 1

#Returns any keys that can be collected given a list of keys you already have
#Path is blocked by locked doors and uncollected keys (if you're passing over
#a key, might as well pick it up. It will never be faster not to, so don't
#bother calculating that possibility)
def available_keys(keys, maze):
    #If there are no more keys to get, return empty list
    if len(keys) == 27:
        return []
    if keys in availcache:
        return availcache[keys]

    tempmaze = [y[:] for y in maze]
    avail = []
    flag = True
    
    while flag:
        for y in range(1, len(tempmaze) - 1):
            for x in range(1, len(tempmaze[0]) - 1):
                if tempmaze[y][x] == '#' or tempmaze[y][x] == '&':
                    continue
                if tempmaze[y][x] == '@':
                    tempmaze[y][x] = '%'
                    continue
                if '&' in adjacent_squares(x, y, tempmaze):
                    if tempmaze[y][x] == '.':
                        tempmaze[y][x] = '%'
                    elif tempmaze[y][x].isupper():
                        if tempmaze[y][x].lower() in keys:
                            tempmaze[y][x] = '%'
                    elif tempmaze[y][x].islower():
                        if tempmaze[y][x] in keys:
                            tempmaze[y][x] = '%'
                        elif not tempmaze[y][x] in avail:
                            avail.append(tempmaze[y][x])
        flag = False
        for y in range(1, len(tempmaze) - 1):
            for x in range(1, len(tempmaze[0]) - 1):
                if tempmaze[y][x] == '%':
                    flag = True
                    tempmaze[y][x] = '&'
    availcache[keys] = avail
    return avail
                

#Recursive function that returns the shortest distance to get all remaining keys
#from a given starting position, taking into account which keys you already have
def distremaining(start, keys, maze, outermost = False):
    if len(keys) == 26:
        return 0
    nextkeys = frozenset(keys | frozenset([start]))
    cachekey = (start, nextkeys)
    if cachekey in remaincache:
        return remaincache[cachekey]
    minlen = 99999999
    for n in available_keys(nextkeys, maze):
        #nkeys = frozenset(nextkeys | frozenset([n]))
        pathlen = distbetween(start, n, maze)+distremaining(n,nextkeys,maze)
        if pathlen < minlen:
            minlen = pathlen
        if outermost:
            print(n, pathlen)
    if outermost:
        print()
    remaincache[cachekey] = minlen
    return minlen

starttime = time.time()        

maze = readmaze('AoC_18-1.txt')
filldeadends(maze)
printmaze(maze)

print(distremaining('@',frozenset([]),maze, outermost = True))
print('Elapsed time: {0:0.3f}s'.format(time.time() - starttime))
