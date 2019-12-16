################################################################################
# AoC_15-1.py
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
################################################################################
import INTCODE_T
from asciimatics.screen import Screen

dirs = [ord('w'),ord('a'),ord('s'),ord('d')]
stepcount = 0

def robo(screen):
    global stepcount
    cpu = INTCODE_T.Intcomp_T(1, 'CPU', 4096)
    cpu.loadfile('REPAIRDROID')
    cpu.start()
    start_pos = [21, 21]
    cur_pos = [21, 21]
    next_pos = [21, 21]
    screen.print_at('D', cur_pos[0], cur_pos[1], 3)
    screen.refresh()
    while True:
        #Handle input
        got_key = False
        inp = screen.get_key()
        if inp == ord('q'):
            got_key = True
            cpu.inQ.put(0)
            break
        elif inp == ord('w'):
            got_key = True
            cpu.inQ.put(1)
            next_pos[1] -= 1
        elif inp == ord('a'):
            got_key = True
            cpu.inQ.put(3)
            next_pos[0] -= 1
        elif inp == ord('s'):
            got_key = True
            cpu.inQ.put(2)
            next_pos[1] += 1
        elif inp == ord('d'):
            got_key = True
            cpu.inQ.put(4)
            next_pos[0] += 1

        #Handle output
        if got_key:
            outp = cpu.outQ.get()
            if outp == 0:
                screen.print_at('█', next_pos[0], next_pos[1], 1)
                next_pos = [i for i in cur_pos]
            elif outp == 1:
                screen.print_at('.', cur_pos[0], cur_pos[1], 7)
                screen.print_at('D', next_pos[0], next_pos[1], 3)
                cur_pos = [i for i in next_pos]
                stepcount += 1
            elif outp == 2:
                screen.print_at('.', cur_pos[0], cur_pos[1], 7)
                screen.print_at('X', next_pos[0], next_pos[1], 2)
                stepcount += 1
                cur_pos = [i for i in next_pos]
        
        if cur_pos[0] != start_pos[0] and cur_pos[1] != start_pos[1]:
            screen.print_at('o', start_pos[0], start_pos[1], 3)

        screen.refresh()

Screen.wrapper(robo)
print(stepcount)
