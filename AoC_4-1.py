################################################################################
# AoC_4-1.py
# 2019-12-04
# Mike Quigley
#
# https://adventofcode.com/2019/day/4
#
# Find how many numbers meet the following criteria:
#  1. Between 134792 and 675810 inclusive
#  2. Contains at least 2 of the same digit
#  3. Each digit is equal to or higher than the digit to its left
################################################################################

def fits(x):
    double = False
    increasing = True
    strX = str(x)
    for i in range(1,6):
        if strX[i-1] == strX[i]:
            double = True
        if strX[i-1] > strX[i]:
            increasing = False
    return double and increasing

matches = [i for i in range(134792, 675811) if fits(i)]
print(matches)
