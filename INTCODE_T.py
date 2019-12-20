################################################################################
# INTCODE_T.py
# 2019-12-11
# Mike Quigley
#
# This variant of the Intcode emulator runs in a threat and uses queues for I/O
# It's a separate file because threads can't be started again after they stop,
# so this version can't run in interactive mode like the other one.
#
# Will send program outputs (opcode 4) to outQ,
# as well as "END" when the program ends
#
# 2019-12-13: Optional prompt for input. Will put "P>" on outQ
# 2019-12-19: Added load function that takes a list of ints. Should be faster
#             than reading from file
#
# Opcode table:
#  1: ADD A B DEST - Adds A + B, result in DEST.
#  2: MUL A B DEST - Multiplies A * B, result in DEST
#  3: INP DEST     - Reads input to DEST
#  4: OUT A        - put A on output queue
#  5: JNZ A B      - If A is not 0, set program counter to B
#  6: JEZ A B      - If A is 0, set program counter to B
#  7: TLT A B DEST - If A < B, store 1 in DEST. Otherwise store 0
#  8: TEQ A B DEST - If A == B, store 1 in DEST. Otherwise store 0
#  9: ARB A        - Add A to relative base
# 99: HALT
################################################################################
import threading
import queue

class Intcomp_T(threading.Thread):

    #mem is RAM size
    def __init__(self, threadID, name, mem, prompt_for_input = False):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.prompt_for_input = prompt_for_input
        self.inQ = queue.Queue()    #Input queue
        self.outQ = queue.Queue()   #Output queue
        self.ram = []               #Main memory
        self.pM = [0, 0, 0]         #Parameter mode flags
        self.pc = 0                 #Program counter
        self.base = 0               #Relative Base
        self.ram = [0 for i in range(mem)]

    #Load program from list of int
    def load(self, program):
        for i in range(len(program)):
            self.ram[i] = program[i]

    #Load program from file
    def loadfile(self, filename):
        file = open(filename,'r')
        prog = file.readline().split(',')
        for i in range(len(prog)):
            self.ram[i] = int(prog[i])
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
                if self.prompt_for_input:
                    self.outQ.put('P>')
                self.write(1, self.inQ.get(True))
                self.pc += 2
            elif op == 4:
                self.outQ.put(self.fetch(1))
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
                self.outQ.put("END")
                halt = True
            else:
                print("ERROR UNKNOWN OPCODE", op, "AT ADDR", self.pc)
                self.outQ.put("END")
                halt = True
