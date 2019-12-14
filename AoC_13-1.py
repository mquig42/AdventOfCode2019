################################################################################
# AoC_13-1.py
# 2019-12-13
# Mike Quigley
#
# https://adventofcode.com/2019/day/13
#
# We're building an arcade cabinet today. The actual game is in Intcode,
# but it needs some outside support.
# Graphics are based on tiles, of which there are 5 different types.
# This program finds the game's screen size, and counts the number of blocks
# (Tile ID 2)
################################################################################
import INTCODE_T

cpu = INTCODE_T.Intcomp_T(1, "CPU", 4096)
cpu.loadfile("ARCADE")
cpu.start()

blocks = 0
coords = [999,999,0,0]
while True:
    x = cpu.outQ.get(True)
    if x == "END":
        break
    y = cpu.outQ.get(True)
    tile = cpu.outQ.get(True)
    
    if tile == 2:
        blocks += 1
    if x < coords[0]:
        coords[0] = x
    if y < coords[1]:
        coords[1] = y
    if x > coords[2]:
        coords[2] = x
    if y > coords[3]:
        coords[3] = y

print(blocks)
print(coords)
