################################################################################
# AoC_18-1.py
# 2019-12-18
# Mike Quigley
#
# https://adventofcode.com/2019/day/18
#
# Variant of part 1's maze. There are 4 separate sections, each with its own
# entrance. In the file AoC_18-2.txt, I have labelled the entrances 0,1,2,3
# according to what quadrant they're in.
#
# Quadrant map:  3 | 0
#                --|--
#                2 | 1
#
# Quadrants are explored by 4 separate robots with shared key inventory
# I guess keys are electronic, and can transfer by WiFi
# As a first attempt, call distremaining separately for each quadrant, and
# give each instance of it any keys which are in other quadrants.
# To do this, we'll need a function that maps out which keys are in which quad.
################################################################################
import time

#Same as previous maze
deaddoors = ['D','I','L','M','O','Q','S','U','W','Z']
keyquads = [[],[],[],[]]

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
                if tempmaze[y][x] in ['0','1','2','3']:
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

#populates the keyquads list, which describes what quad each key is located in
def mapkeys(maze):
    halfx = len(maze[0])//2
    halfy = len(maze)//2
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x].islower():
                if x > halfx and y < halfy:
                    keyquads[0].append(maze[y][x])
                elif x > halfx and y > halfy:
                    keyquads[1].append(maze[y][x])
                elif x < halfx and y > halfy:
                    keyquads[2].append(maze[y][x])
                elif x < halfx and y < halfy:
                    keyquads[3].append(maze[y][x])
                else:
                    print("ERROR", maze[y][x])

starttime = time.time()        

maze = readmaze('AoC_18-2.txt')
filldeadends(maze)
printmaze(maze)
mapkeys(maze)

key0 = frozenset(keyquads[1]+keyquads[2]+keyquads[3])
key1 = frozenset(keyquads[0]+keyquads[2]+keyquads[3])
key2 = frozenset(keyquads[0]+keyquads[1]+keyquads[3])
key3 = frozenset(keyquads[0]+keyquads[1]+keyquads[2])

totaldist = distremaining('0',key0,maze)
totaldist += distremaining('1',key1,maze)
totaldist += distremaining('2',key2,maze)
totaldist += distremaining('3',key3,maze)
print(totaldist)
print('Elapsed time: {0:0.3f}s'.format(time.time() - starttime))
