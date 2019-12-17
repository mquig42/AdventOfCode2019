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
#
# This program, as-is, should produce the correct answer given enough time
# but that could be hours (Actually about 19 years).
# The FFT algorithm is n^2, so running it on large inputs will never be
# practical. Maybe there's a pattern?
################################################################################
import time
import io

#This cache reduces runtime from 14 seconds to 6
#Unfortunately, it's only useful on small inputs. There isn't enough
#RAM when input length is 6.5 million
patterncache = dict()

#Generates the multiplier pattern
def getpattern(digit, length):
    if digit in patterncache:
        return patterncache[digit]
    
    pattern = [0, 1, 0, -1]
    r = []
    while len(r) < length+1:
        for i in range(len(pattern)):
            for j in range(digit+1):
                r.append(pattern[i])
                
    patterncache[digit] = r[1:length+1]
    return r[1:length+1]

def fft(inp):
    r = []
    for i in range(len(inp)):
        pattern = getpattern(i, len(inp))
        x = 0
        for j in range(len(inp)):
            x += inp[j]*pattern[j]
        x = abs(x)%10
        r.append(x)
    return r

def printdigits(digits, length):
    for i in range(length):
        print(digits[i], end='')
    print()

start_time = time.time()

file = open('AoC_16.txt','r')
inpstr = '123'
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
    inp=fft(inp)
    print(i, '% complete')

printdigits(inp[offset:offset+8],8)
print('Elapsed Time:', '{0:0.3f}s'.format(time.time() - start_time))
