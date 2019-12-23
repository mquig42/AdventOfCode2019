################################################################################
# AoC_22-2.py
# 2019-12-22
# Mike Quigley
#
# https://adventofcode.com/2019/day/22#part2
#
# Shuffle a bigger deck a large number of times
# If your computer is listed on top500.org, you might actually be able
# to run this program.
################################################################################
import time

class spacedeck:
    def __init__(self, size=10007):
        self.deck = [i for i in range(size)]

    def __str__(self):
        return str(self.deck)

    def newstack(self):
        self.deck.reverse()

    def cut(self, n):
        n = n % len(self.deck)
        self.deck = self.deck[n:] + self.deck[:n]

    def deal(self, inc):
        size = len(self.deck)
        table = [' ' for i in range(size)]
        i = 0
        while(len(self.deck) > 0):
            table[i] = self.deck.pop(0)
            i = (i + inc) % size
        self.deck = table

    def card_at(self, n):
        return self.deck[n]

    def index(self, n):
        return self.deck.index(n)
        
starttime = time.time()

sd = spacedeck(119315717514047)

file = open('AoC_22.txt','r')
instructions = [line.strip() for line in file]
file.close()

for i in range(101741582076661):
    for line in instructions:
        if line == 'deal into new stack':
            sd.newstack()
        elif line.startswith('cut'):
            sd.cut(int(line.replace('cut ','')))
        elif line.startswith('deal with increment'):
            sd.deal(int(line.replace('deal with increment ','')))

print(sd.card_at(2020))
print('Elapsed time: {0:0.3f}s'.format(time.time()-starttime))
