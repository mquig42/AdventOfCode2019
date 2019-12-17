################################################################################
# AoC_16-2.py
# 2019-12-16
# Mike Quigley
#
# https://adventofcode.com/2019/day/16
#
# Part 2 has only 2 changes from part 1. The final message we want to print
# is taken from the middle of the digit list, not the beginning.
# Also, we need to concatenate the input 10,000 times. Part 1 takes 14 seconds
# to run on the input as given, so this needs improvement.
################################################################################
import time
import io

#Shortcut that only gets the second half of the data correct
def fft(inp):
    s = 0
    for i in range(len(inp)-1,-1,-1):
        s += inp[i]
        inp[i] = s % 10

def printdigits(digits, length):
    for i in range(length):
        print(digits[i], end='')
    print()

start_time = time.time()

file = open('AoC_16.txt','r')
inpstr = file.readline()
file.close()

#Concatenate
buffer = io.StringIO()
for i in range(10000):
    buffer.write(inpstr)
inpstr = buffer.getvalue()
buffer.close()

offset = int(inpstr[0:7])
inp = [int(c) for c in inpstr]

for i in range(100):
    fft(inp)
    print(i, '% complete')

printdigits(inp[offset:offset+8],8)
print('Elapsed Time:', '{0:0.3f}s'.format(time.time() - start_time))
