################################################################################
# AoC_24-2.py
# 2019-12-27
# Mike Quigley
#
# https://adventofcode.com/2019/day/24
#
# Cellular automaton
# This time, it's in infinitely recursive space, like the portal maze
# Most cells are adjacent to cells on other levels
################################################################################
from asciimatics.screen import Screen
import time

#Store state as a dict, so depth index can be negative
curstate = dict()

#Adjacency list.
adjlist = [[(-1,7),(0,1),(0,5),(-1,11)],    #0
           [(-1,7),(0,2),(0,6),(0,0)],      #1
           [(-1,7),(0,3),(0,7),(0,1)],      #2
           [(-1,7),(0,4),(0,8),(0,2)],      #3
           [(-1,7),(-1,13),(0,9),(0,3)],    #4
           [(0,0),(0,6),(0,10),(-1,11)],    #5
           [(0,1),(0,7),(0,11),(0,5)],      #6
           [(0,2),(0,8),(1,0),(1,1),(1,2),(1,3),(1,4),(0,6)],           #7
           [(0,3),(0,9),(0,13),(0,7)],      #8
           [(0,4),(-1,13),(0,14),(0,8)],    #9
           [(0,5),(0,11),(0,15),(-1,11)],   #10
           [(0,6),(1,0),(1,5),(1,10),(1,15),(1,20),(0,16),(0,10)],      #11
           [],                              #There is no 12
           [(0,8),(0,14),(0,18),(1,4),(1,9),(1,14),(1,19),(1,24)],      #13
           [(0,9),(-1,13),(0,19),(0,13)],   #14
           [(0,10),(0,16),(0,20),(-1,11)],  #15
           [(0,11),(0,17),(0,21),(0,15)],   #16
           [(1,20),(1,21),(1,22),(1,23),(1,24),(0,18),(0,22),(0,16)],   #17
           [(0,13),(0,19),(0,23),(0,17)],   #18
           [(0,14),(-1,13),(0,24),(0,18)],  #19
           [(0,15),(0,21),(-1,17),(-1,11)], #20
           [(0,16),(0,22),(-1,17),(0,20)],  #21
           [(0,17),(0,23),(-1,17),(0,21)],  #22
           [(0,18),(0,24),(-1,17),(0,22)],  #23
           [(0,19),(-1,13),(-1,17),(0,23)]] #24

def bugs(screen):
    for t in range(200):
        updstate()
        for x in range(5):
            for y in range(5):
                screen.print_at('█' if getcell_xy(x,y) == '#' else ' ',x,y,2)
        screen.refresh()
        time.sleep(0.25)

def updstate():
    global curstate

    #Generate new state
    nextstate = dict()
    for r in range(min(curstate.keys()) - 1, max(curstate.keys()) + 2):
        nextr = [' ' for i in range(25)]
        for n in range(25):
            if getcell_rn(r, n) == '#':
                nextr[n] = '#' if adj(r,n) == 1 else '.'
            else:
                nextr[n] = '#' if adj(r,n) in [1,2] else '.'
        nextstate[r] = ''.join(nextr)

    #If the top or bottom level is empty, remove it
    if nextstate[min(nextstate.keys())] == '.....':
        del nextstate[min(nextstate.keys())]
    if nextstate[max(nextstate.keys())] == '.....':
        del nextstate[max(nextstate.keys())]
    curstate = nextstate

#Gets a cell from level 0 using x and y coords. Used for drawing
def getcell_xy(x, y):
    return curstate[0][5*y + x]

#Gets a cell by recursion level and number
def getcell_rn(r, n):
    if not r in curstate:
        return '.'
    return curstate[r][n]

#Returns number of bugs adjacent to a space
def adj(r, n):
    c = 0
    for a in adjlist[n]:
        if getcell_rn(r+a[0],a[1]) == '#':
            c += 1
    return c

#Returns total number of bugs in all levels
def bugcount():
    c = 0
    for r in curstate.values():
        for n in r:
            if n == '#':
                c += 1
    return c

def printlevel(r):
    print(curstate[r][:5])
    print(curstate[r][5:10])
    print(curstate[r][10:15])
    print(curstate[r][15:20])
    print(curstate[r][20:25])

file = open('Aoc_24.txt','r')
curstate[0] = ''
for line in file:
    curstate[0] += line.strip()
file.close()
#for i in range(200):
#    updstate()
Screen.wrapper(bugs)
print(bugcount())
