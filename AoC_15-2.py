################################################################################
# AoC_15-2.py
# 2019-12-15
# Mike Quigley
#
# https://adventofcode.com/2019/day/15
#
# Control a repair droid to locate the oxygen system
# The Intcode program will take one input, representing a direction to move,
# and return one output, representing a status code
#
# Directions:       Status codes:
#  1 North           0 Wall
#  2 South           1 Successful move
#  3 West            2 Found objective
#  4 East
#
# The maze is a 41x41 square, with the start position at (21, 21)
# For part 2, explore the maze automatically, then figure out how long
# it will take to fill with oxygen once the system is repaired
################################################################################
import INTCODE_T
import random
import time
from asciimatics.screen import Screen

#This program's direction codes are not in order. Use this array
#so we can store direction in clockwise format, and turn left or right with math
dirs = [1, 4, 2, 3]

#Store map of maze here
maze = [[' ' for x in range(41)] for y in range(41)]

def robo(screen):
    global maze
    cpu = INTCODE_T.Intcomp_T(1, 'CPU', 4096)
    cpu.loadfile('REPAIRDROID')
    cpu.start()
    
    cur_pos = [21, 21]
    next_pos = [21, 21]
    goal = [0,0]        #Currently unknown
    direction = 0
    at_goal = False
    turned_left = False
    
    screen.print_at('D', cur_pos[0], cur_pos[1], 3)
    screen.refresh()

    #Phase 1: map the maze
    while True:
        #Automatic mapping algorithm
        #Square to the left can be open, wall, or unknown
        #If wall, continue straight
        #Otherwise, change direction to the left
        #If path ahead is also a wall, turn right
        if left_square(cur_pos[0], cur_pos[1], direction) != '█':
            direction = (direction + 1) % 4
            turned_left = True
        elif ahead_square(cur_pos[0], cur_pos[1], direction) == '█':
            direction = (direction - 1) % 4
        cpu.inQ.put(dirs[direction])
        if dirs[direction] == 1:
            next_pos[1] -= 1
        elif dirs[direction] == 2:
            next_pos[1] += 1
        elif dirs[direction] == 3:
            next_pos[0] -= 1
        elif dirs[direction] == 4:
            next_pos[0] += 1

        #Handle output
        outp = cpu.outQ.get()
        if outp == 0:
            screen.print_at('█', next_pos[0], next_pos[1], 1)
            maze[next_pos[0]][next_pos[1]] = '█'
            next_pos = [i for i in cur_pos]
            #If we just turned left and bumped into a wall, that means there was
            #a wall to our left. Turn right to keep going in previous direction
            if turned_left:
                direction = (direction - 1) % 4
        elif outp == 1:
            screen.print_at('D', next_pos[0], next_pos[1], 3)
            if not at_goal:
                screen.print_at('.', cur_pos[0], cur_pos[1], 7)
                maze[next_pos[0]][next_pos[1]] = '.'
            cur_pos = [i for i in next_pos]
            at_goal = False
        elif outp == 2:
            screen.print_at('.', cur_pos[0], cur_pos[1], 7)
            screen.print_at('X', next_pos[0], next_pos[1], 2)
            maze[next_pos[0]][next_pos[1]] = 'X'
            cur_pos = [i for i in next_pos]
            goal = [i for i in next_pos]
            at_goal = True

        screen.refresh()

        if is_mapped():
            cpu.inQ.put(0)
            break

    #Phase 2: flood with oxygen
    minutes = 0
    maze[goal[0]][goal[1]] = 'O'
    screen.print_at('█', goal[0], goal[1], 4)
    screen.refresh()
    while not flood(screen):
        time.sleep(0.02)
        minutes += 1
        screen.refresh()

    print(minutes)
    
#d: 0=N, 1=E, 2=S, 3=W
def left_square(x, y, d):
    global maze
    if d == 0:
        return maze[x+1][y]
    elif d == 1:
        return maze[x][y+1]
    elif d == 2:
        return maze[x-1][y]
    elif d == 3:
        return maze[x][y-1]

def ahead_square(x, y, d):
    return left_square(x, y, (d-1)%4)

def adjacent_squares(x, y):
    global maze
    return [maze[x][y-1],
            maze[x+1][y],
            maze[x][y+1],
            maze[x-1][y]]

def is_mapped():
    global maze
    if maze[21][21] != '.':
        return False
    for x in range(41):
        for y in range(41):
            if maze[x][y] == '.' and ' ' in adjacent_squares(x, y):
                return False
    return True

#Return value: is maze fully flooded
def flood(screen):
    global maze
    r = True
    for x in range(41):
        for y in range(41):
            if maze[x][y] == '.' and 'O' in adjacent_squares(x,y):
                maze[x][y] = 'N'
                screen.print_at('█', x, y, 4)

    for x in range(41):
        for y in range(41):
            if maze[x][y] == 'N':
                maze[x][y] = 'O'
                r = False
    return r
    

Screen.wrapper(robo)

#Print maze
for y in range(41):
    for x in range(41):
        print(maze[x][y],end='')
    print()
