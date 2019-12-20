################################################################################
# AoC_19-2.py
# 2019-12-19
# Mike Quigley
#
# https://adventofcode.com/2019/day/19#Part2
#
# The beam spreads out as it gets farther away. Find the closest point where
# a 100x100 square will be entirely enclosed by it.
# Return the coords of the top left corner
#
# No ASCII graphics for this one, it's too big.
#
# According to the beamwidth() function, the first row with a beam width of 100
# is 712, where the beam spans from 397 to 497
#
# This runs in 347 seconds on my PC, so a bit slow but it finds the right answer
################################################################################
import INTCODE_T
import time

beamcache = dict()
progcache = []

#Returns result of TRACTORBEAM program for point (x, y)
def isbeam(x, y):
    if (x, y) in beamcache:
        return beamcache[(x, y)]
    
    cpu = INTCODE_T.Intcomp_T(1, 'cpu', 1024)
    cpu.load(progcache)
    cpu.start()
    cpu.inQ.put(x)
    cpu.inQ.put(y)
    r = cpu.outQ.get()
    
    beamcache[(x, y)] = r
    return r

#Returns True if a 100x100 square will be entirely enclosed by the tractor beam
#when the top left corner is at point (x, y)
def squarefits(x, y):
    #Check corners
    if not isbeam(x, y):
        return False
    if not isbeam(x+99,y):
        return False
    if not isbeam(x, y+99):
        return False
    if not isbeam(x+99, y+99):
        return False

    #Now check whole range
    for a in range(x, x+100):
        for b in range(y, y+100):
            if not isbeam(a, b):
                return False

    return True

#Returns smallest x-coord of a fitting square at given y coord
#or 0 if no square fits
def square_minx(y):
    minx, maxx = beamwidth(y)
    for x in range(minx, maxx):
        if squarefits(x, y):
            return x
    return 0

#Returns the start and end points of a beam slice at given y coord
#Do not call this where there is no beam, it will infinite loop
def beamwidth(y):
    start = 0
    end = 0
    x = 0
    while end == 0:
        b = isbeam(x, y)
        if b == 1 and start == 0:
            start = x
        if b == 0 and start != 0:
            end = x - 1
        x += 1
    return start, end
    

file = open('TRACTORBEAM','r')
progstr = file.readline().split(',')
progcache = [int(c) for c in progstr]
file.close()

starttime = time.time()

for y in range(700, 2000):
    x = square_minx(y)
    if x != 0:
        print(x, y)
        break

print('Elapsed Time:', '{0:0.3f}s'.format(time.time() - starttime))

