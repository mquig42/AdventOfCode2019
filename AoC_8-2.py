################################################################################
# AoC_8-2.py
# 2019-12-08
# Mike Quigley
#
# https://adventofcode.com/2019/day/8
#
# Input is a string of numbers representing an image. Each number is one pixel,
# the sequence goes left to right, then top to bottom. There are multiple layers
#
# Decode the image. 0 is a black pixel, 1 is white, and 2 is transparent
################################################################################

width = 25
height = 6
layersize = width * height

def findpixelvalue(i, img, layercount):
    for j in range(layercount):
        if img[j][i] != '2':
            return img[j][i]

file = open("AoC_8-1.txt","r")
data = file.read()
file.close()

layercount = len(data)//(layersize)
layers = []

#split data into list of layers
for i in range(layercount):
    layers.append(list(data[i*layersize:i*layersize + layersize]))

#now merge
for i in range(layersize):
    if layers[0][i] == '2':
        layers[0][i] = findpixelvalue(i, layers, layercount)

#Display image
for i in range(height):
    for p in layers[0][i*width:i*width+width]:
        print('█' if p == '0' else ' ', end='')
    print()
