################################################################################
# AoC_19-1.py
# 2019-12-19
# Mike Quigley
#
# https://adventofcode.com/2019/day/19
#
# Tractor beam calibration test
# The TRACTORBEAM Intcode program takes 2 inputs for x and y coords
# and returns either 0 or 1. Find the number of 1s for x and y values
# between 0 and 49
################################################################################
import INTCODE_T
from asciimatics.screen import Screen
import time

def beamtest(screen):
    counter = 0
    for y in range(50):
        for x in range(50):
            cpu = INTCODE_T.Intcomp_T(1,'cpu',4096)
            cpu.loadfile('TRACTORBEAM')
            cpu.start()
            cpu.inQ.put(x)
            cpu.inQ.put(y)
            r = cpu.outQ.get()
            if r == 0:
                screen.print_at('.',x,y,7)
            else:
                screen.print_at('#',x,y,4)
                counter += 1
            time.sleep(0.02)
            screen.refresh()
    screen.print_at(str(counter),0,52,7)
    screen.refresh()
    while True:
        k = screen.get_key()
        if k == ord('q'):
            break

Screen.wrapper(beamtest)
