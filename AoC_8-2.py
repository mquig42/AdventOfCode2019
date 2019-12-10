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

def printpixel(i, img, layercount):
    for j in range(layercount):
        if img[j][i] != '2':
            print('█' if img[j][i] == '0' else ' ', end='')
            return

file = open("AoC_8-1.txt","r")
data = list(file.read())
file.close()

layercount = len(data)//(layersize)
layers = [data[i*layersize:(i+1)*layersize] for i in range(layercount)]

for i in range(layersize):
    printpixel(i,layers,layercount)
    print(end = '\n' if (i+1)%width==0 else '')
