################################################################################
# AoC_4-2.py
# 2019-12-04
# Mike Quigley
#
# https://adventofcode.com/2019/day/4#part2
#
# Find how many numbers meet the following criteria:
#  1. Between 134792 and 675810 inclusive
#  2. Contains exactly 2 of the same digit
#  3. Each digit is equal to or higher than the digit to its left
################################################################################

def fits(x):
    increasing = True
    counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    strX = str(x)
    for i in range(0,6):
        if i > 0 and strX[i-1] > strX[i]:
            increasing = False
        counts[int(strX[i])] += 1
    return increasing and (2 in counts)

matches = [i for i in range(134792, 675811) if fits(i)]
print(len(matches))
