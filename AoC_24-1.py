################################################################################
# AoC_24-1.py
# 2019-12-27
# Mike Quigley
#
# https://adventofcode.com/2019/day/24
#
# Cellular automaton
# Find the first state to repeat and compute a checksum
################################################################################
from asciimatics.screen import Screen
import time

prevstates = set()
curstate = ''

def bugs(screen):
    final = False
    while not final:
        final = updstate()
        for x in range(5):
            for y in range(5):
                screen.print_at('█' if getcell(x, y) == '#' else ' ', x, y, 2)
        screen.refresh()
        time.sleep(0.25)

def updstate():
    global curstate
    if curstate in prevstates:
        printstate()
        print(rating())
        return True
    prevstates.add(curstate)
    nextstate = [' ' for i in range(25)]
    for x in range(5):
        for y in range(5):
            if getcell(x, y) == '#':
                nextstate[5*y+x] = '#' if adj(x, y) == 1 else '.'
            else:
                nextstate[5*y+x] = '#' if adj(x,y) in [1,2] else '.'
    curstate = ''.join(nextstate)
    return False

def getcell(x, y):
    if x < 0 or x > 4 or y < 0 or y > 4:
        return '.'
    i = 5*y + x
    if 0 <= i < 25:
        return curstate[i]
    return '.'

#Returns number of bugs adjacent to a space
def adj(x, y):
    r = [getcell(x-1, y),
         getcell(x, y-1),
         getcell(x+1, y),
         getcell(x, y+1)]
    s = 0
    for i in r:
        if i == '#':
            s += 1
    return s

def printstate():
    for y in range(5):
        for x in range(5):
            print(getcell(x,y),end='')
        print()

def printadj():
    for y in range(5):
        for x in range(5):
            print(adj(x,y),end='')
        print()

def rating():
    s = 0
    for i in range(25):
        if curstate[i] == '#':
            s += 2**i
    return s

file = open('Aoc_24.txt','r')
for line in file:
    curstate += line.strip()
file.close()
Screen.wrapper(bugs)
