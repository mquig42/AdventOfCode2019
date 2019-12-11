################################################################################
# AoC_11-1.py
# 2019-12-11
# Mike Quigley
#
# Use an Intcode machine as the brain of a painting robot
# (Similar to a LOGO turtle)
# The PAINT program will repeatedly take one input value from the robot's camera
# 0 if it's on a black square, 1 for white
# then output 2 numbers. The first is a colour value, the second is a direction
# 0 to turn 90 degrees left, 1 to turn 90 degrees right. Robot always moves
# 1 space forward after each instruction
#
# Opcode table:
#  1: ADD A B DEST - Adds A + B, result in DEST.
#  2: MUL A B DEST - Multiplies A * B, result in DEST
#  3: INP DEST     - Reads keyboard input to DEST
#  4: OUT A        - Print A
#  5: JNZ A B      - If A is not 0, set program counter to B
#  6: JEZ A B      - If A is 0, set program counter to B
#  7: TLT A B DEST - If A < B, store 1 in DEST. Otherwise store 0
#  8: TEQ A B DEST - If A == B, store 1 in DEST. Otherwise store 0
#  9: ARB A        - Add A to relative base
# 99: HALT
################################################################################
import threading
import queue

#Program I/O queues
inQ = queue.Queue()     #Program input
outQ = queue.Queue()    #Program output

#Robot position and state
grid = [['.' for y in range(160)] for x in range(160)]
pos = [80,80]
dirs = ['U','R','D','L']
d = 0

class Intcomp(threading.Thread):

    #mem is RAM size
    def __init__(self, threadID, name, mem):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ram = []
        self.pM = [0, 0, 0]     #Parameter mode flags
        self.pc = 0             #Program counter
        self.base = 0           #Relative Base
        self.ram = [0 for i in range(mem)]

    #Dumps memory to screen
    def list(self):
        for i in range(0,len(self.ram),4):
            print("{0:4d}: {1}".format(i,self.ram[i:i+4]))

    #Sets all memory to 0
    def clear(self):
        self.ram = [0 for i in range(len(self.ram))]
        self.base = 0

    #Load program from console
    def load(self, program):
        pL = program.split(',')
        for i in range(0,len(pL)):
            self.ram[i] = int(pL[i])

    #Load program from file
    def loadfile(self, filename):
        file = open(filename,'r')
        self.load(file.readline())
        file.close()

    #Fetch value from RAM. Behaviour governed by mode flag
    def fetch(self, param):
        if self.pM[param - 1] == 0:
            return self.ram[self.ram[self.pc + param]]
        elif self.pM[param - 1] == 1:
            return self.ram[self.pc + param]
        elif self.pM[param - 1] == 2:
            return self.ram[self.ram[self.pc + param] + self.base]

    #Writes value to RAM. Behaviour governed by mode flag
    def write(self, param, value):
        if self.pM[param - 1] == 0:
            self.ram[self.ram[self.pc+param]] = value
        elif self.pM[param - 1] == 2:
            self.ram[self.ram[self.pc+param] + self.base] = value

    #Run program
    def run(self):
        halt = False
        self.pc = 0
        op = 0
        while not halt:
            op = self.ram[self.pc] % 100
            self.pM[0] = (self.ram[self.pc] // 100) % 10
            self.pM[1] = (self.ram[self.pc] // 1000) % 10
            self.pM[2] = (self.ram[self.pc] // 10000) % 10
            if op == 1:
                self.write(3, self.fetch(1) + self.fetch(2))
                self.pc += 4
            elif op == 2:
                self.write(3, self.fetch(1) * self.fetch(2))
                self.pc += 4
            elif op == 3:
                self.write(1, inQ.get(True))
                self.pc += 2
            elif op == 4:
                outQ.put(self.fetch(1))
                self.pc += 2
            elif op == 5:
                self.pc = self.fetch(2) if self.fetch(1) != 0 else self.pc + 3
            elif op == 6:
                self.pc = self.fetch(2) if self.fetch(1) == 0 else self.pc + 3
            elif op == 7:
                self.write(3, 1 if self.fetch(1) < self.fetch(2) else 0)
                self.pc += 4
            elif op == 8:
                self.write(3, 1 if self.fetch(1) == self.fetch(2) else 0)
                self.pc += 4
            elif op == 9:
                self.base += self.fetch(1)
                self.pc += 2
            elif op == 99:
                outQ.put(99)
                halt = True
            else:
                print("ERROR UNKNOWN OPCODE", op, "AT ADDR", self.pc)
                outQ.put(99)
                halt = True

#Robot code

#If I only had a brain
comp = Intcomp(1, "BRAIN", 4096)
comp.loadfile("PAINT")
comp.start()

paintedSquares = dict()

while True:
    inQ.put(0 if grid[pos[0]][pos[1]] == '.' else 1)
    colour = outQ.get(True)
    if colour == 99:
        break
    grid[pos[0]][pos[1]] = '.' if colour == 0 else '#'
    paintedSquares[(pos[0],pos[1])] = grid[pos[0]][pos[1]]
    turn = outQ.get(True)
    if turn == 99:
        break
    d = (d + (turn * 2 - 1)) % 4
    if d == 0:
        pos[1] -= 1
    elif d == 1:
        pos[0] += 1
    elif d == 2:
        pos[1] += 1
    elif d == 3:
        pos[0] -= 1

#Print finished grid
for y in range(len(grid[0])):
    for x in range(len(grid)):
        print(grid[x][y], end='')
    print()
print(len(paintedSquares), "SQUARES PAINTED")
