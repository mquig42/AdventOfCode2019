################################################################################
# AoC_7-2.py
# 2019-12-05
# Mike Quigley
#
# Run 5 instances of the AMPLIFIER program in feedback mode. This requires
# all instances to run concurrently and communicate with each other
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
# 99: HALT
################################################################################
import itertools
import operator
import threading
import queue

itcQ = [queue.Queue(),queue.Queue(),queue.Queue(),queue.Queue(),queue.Queue()]
endQ = [queue.Queue(),queue.Queue(),queue.Queue(),queue.Queue(),queue.Queue()]
currentSetting = (0,0,0,0,0)
results = dict()

class Intcomp(threading.Thread):

    #mem is RAM size
    def __init__(self, threadID, name, mem):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.ram = []
        self.pM = [0, 0, 0]     #Parameter mode flags
        self.pc = 0             #Program counter
        for i in range(0, mem):
            self.ram.append(0)

    #Dumps memory to screen
    def list(self):
        for i in range(0,len(self.ram),4):
            print("{0:4d}: {1}".format(i,self.ram[i:i+4]))

    #Sets all memory to 0
    def clear(self):
        for i in range(0,len(self.ram)):
            self.ram[i] = 0

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

    #Fetch value from RAM. Will dereference pointers if mode flag is 0
    def fetch(self, param):
        if self.pM[param - 1] == 0:
            return self.ram[self.ram[self.pc + param]]
        else:
            return self.ram[self.pc + param]

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
                self.ram[self.ram[self.pc+3]] = self.fetch(1) + self.fetch(2)
                self.pc += 4
            elif op == 2:
                self.ram[self.ram[self.pc+3]] = self.fetch(1) * self.fetch(2)
                self.pc += 4
            elif op == 3:
                self.ram[self.ram[self.pc+1]] = itcQ[self.threadID].get(True)
                self.pc += 2
            elif op == 4:
                if self.threadID == 4:
                    results[currentSetting] = self.fetch(1)
                    itcQ[0].put(self.fetch(1))
                else:
                    itcQ[self.threadID+1].put(self.fetch(1))
                self.pc += 2
            elif op == 5:
                self.pc = self.fetch(2) if self.fetch(1) != 0 else self.pc + 3
            elif op == 6:
                self.pc = self.fetch(2) if self.fetch(1) == 0 else self.pc + 3
            elif op == 7:
                self.ram[self.ram[self.pc+3]] = 1 if self.fetch(1) < self.fetch(2) else 0
                self.pc += 4
            elif op == 8:
                self.ram[self.ram[self.pc+3]] = 1 if self.fetch(1) == self.fetch(2) else 0
                self.pc += 4
            elif op == 99:
                endQ[self.threadID].put(1)
                halt = True
            else:
                print("ERROR UNKNOWN OPCODE", op, "AT ADDR", self.pc, "IN THREAD", self.name)
                halt = True
        
def findmaxamp():
    global currentSetting
    names = ["A","B","C","D","E"]

    phaseSettings = list(itertools.permutations([9,8,7,6,5]))
    for setting in phaseSettings:
        comps = []
        currentSetting = setting
        for i, s in zip(range(5),setting):
            comps.append(Intcomp(i, names[i], 2048))
            comps[i].loadfile("AMPLIFIER")
            comps[i].start()
            itcQ[i].put(s)
        itcQ[0].put(0)
        for nQ in endQ:
            #Read from all end queues to block until threads end
            nQ.get(True)
        for i in range(5):
            #Inter-thread queues weren't always clear after their thread ended.
            #Reset them here.
            itcQ[i] = queue.Queue()
    print(max(results.items(), key=operator.itemgetter(1)))
    
findmaxamp()
