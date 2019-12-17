################################################################################
# AoC_16-1.py
# 2019-12-16
# Mike Quigley
#
# https://adventofcode.com/2019/day/16
#
# Use the FFT algorithm (no, not that one) on a large number representing a
# radio signal. See web site for description, it's too much to retype here.
################################################################################
import time

#Generates the multiplier pattern
def getpattern(digit, length):
    pattern = [0, 1, 0, -1]
    r = []
    while len(r) < length+1:
        for i in range(len(pattern)):
            for j in range(digit+1):
                r.append(pattern[i])
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
inp = [int(c) for c in file.readline()]
file.close()

for i in range(100):
    inp=fft(inp)

printdigits(inp,8)
print('Elapsed Time:', '{0:0.3f}s'.format(time.time() - start_time))
printdigits(inp,len(inp))
