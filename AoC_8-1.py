################################################################################
# AoC_8-1.py
# 2019-12-08
# Mike Quigley
#
# https://adventofcode.com/2019/day/8
#
# Input is a string of numbers representing an image. Each number is one pixel,
# the sequence goes left to right, then top to bottom. There are multiple layers
# Find the layer with the fewest 0s, then multiply the number of 1s
# by the number of 2s.
#
# The test data only contains the digits 0, 1, and 2
# Let's assume that this format doesn't use any other values
################################################################################

width = 25
height = 6

file = open("AoC_8-1.txt","r")
data = file.read()
file.close()

layercount = len(data)//(width*height)
pixcounts = []

for i in range(layercount):
    pixcounts.append([0,0,0])
    for j in range(width*height):
        pixcounts[i][int(data[j+width*height*i])] += 1

#This will print several numbers. The last one is the correct answer
fewestzero = 99999
for i in range(layercount):
    if pixcounts[i][0] < fewestzero:
        fewestzero = pixcounts[i][0]
        print(pixcounts[i][1] * pixcounts[i][2])
