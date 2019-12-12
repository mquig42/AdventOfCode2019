################################################################################
# AoC_11-2.py
# 2019-12-11
# Mike Quigley
#
# Use an Intcode machine as the brain of a painting robot
# (Similar to a LOGO turtle)
# The PAINT program will repeatedly take one input value from the robot's camera
# 0 if it's on a black square, 1 for white
# then output 2 numbers. The first is a colour value, the second is a direction
# 0 to turn 90 degrees left, 1 to turn 90 degrees right. Robot always moves
# 1 space forward after each instruction
#
# Start on a white panel to actually draw a registration number
#
# Opcode table:
#  1: ADD A B DEST - Adds A + B, result in DEST.
#  2: MUL A B DEST - Multiplies A * B, result in DEST
#  3: INP DEST     - Reads keyboard input to DEST
#  4: OUT A        - Print A
#  5: JNZ A B      - If A is not 0, set program counter to B
#  6: JEZ A B      - If A is 0, set program counter to B
#  7: TLT A B DEST - If A < B, store 1 in DEST. Otherwise store 0
#  8: TEQ A B DEST - If A == B, store 1 in DEST. Otherwise store 0
#  9: ARB A        - Add A to relative base
# 99: HALT
################################################################################
import threading
import queue
import INTCODE_T

#Robot position and state
grid = [['.' for y in range(6)] for x in range(43)]
pos = [0,0]
grid[0][0] = '#'
dirs = ['U','R','D','L']
d = 0

#Init brain
comp = INTCODE_T.Intcomp_T(1, "BRAIN", 4096)
comp.loadfile("PAINT")
comp.start()

paintedSquares = dict()

while True:
    comp.inQ.put(0 if grid[pos[0]][pos[1]] == '.' else 1)
    colour = comp.outQ.get(True)
    if colour == "END":
        break
    grid[pos[0]][pos[1]] = '.' if colour == 0 else '#'
    paintedSquares[(pos[0],pos[1])] = grid[pos[0]][pos[1]]
    turn = comp.outQ.get(True)
    if turn == "END":
        break
    d = (d + (turn * 2 - 1)) % 4
    if d == 0:
        pos[1] -= 1
    elif d == 1:
        pos[0] += 1
    elif d == 2:
        pos[1] += 1
    elif d == 3:
        pos[0] -= 1

#Print finished grid
for y in range(len(grid[0])):
    for x in range(len(grid)):
        print('█' if grid[x][y] == '#' else ' ', end='')
    print()
print(len(paintedSquares), "SQUARES PAINTED")
