################################################################################
# AoC_13-2.py
# 2019-12-13
# Mike Quigley
#
# https://adventofcode.com/2019/day/13
#
# We're building an arcade cabinet today. The actual game is in Intcode,
# but it needs some outside support.
# This program plays the game
################################################################################
import INTCODE_T
from asciimatics.screen import Screen
import time

cpu = INTCODE_T.Intcomp_T(1, "CPU", 4096, True)
tiles = [' ','X','B','=','o']
colours = [0,1,2,7,3]
score = 0

def arcade(screen):
    global score
    screen_complete = False
    ballX = 0
    paddleX = 0
    print("START")
    while True:
        x = cpu.outQ.get(True)
        if x == "END":
            return
        if x == "P>":
            #This game is tricky.
            #De-comment this to have the paddle auto-track the ball
            #if paddleX < ballX:
            #    cpu.inQ.put(1)
            #elif paddleX > ballX:
            #    cpu.inQ.put(-1)
            #else:
            #    cpu.inQ.put(0)
            screen.wait_for_input(5)
            joy = screen.get_key()
            if joy == ord('a'):
                cpu.inQ.put(-1)
            elif joy == ord('d'):
                cpu.inQ.put(1)
            else:
                cpu.inQ.put(0)
            time.sleep(0.2)
            continue
        y = cpu.outQ.get(True)
        tile = cpu.outQ.get(True)

        if x == -1:
            score = tile
            screen_complete = True
            screen.print_at('{0}'.format(tile), 0, 25, colour=7)
        else:
            if tile == 3:
                paddleX = x
            if tile == 4:
                ballX = x
            screen.print_at(tiles[tile], x, y, colour=colours[tile])
        
        if screen_complete:
            #if cpu.waiting:
            #    joy = screen.get_key()
            #    if joy == ord('a'):
            #        cpu.inQ.put(-1)
            #    elif joy == ord('d'):
            #        cpu.inQ.put(1)
            #    elif joy == None:
            #        cpu.inQ.put(0)
            #    elif joy == ord('q'):
            #        return   
            screen.refresh()
            

cpu.loadfile("ARCADE")
cpu.ram[0] = 2
cpu.start()
Screen.wrapper(arcade)
print("Game Over")
print("Your score was:", score)
