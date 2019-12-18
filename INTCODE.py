################################################################################
# INTCODE.py
# 2019-12-05
# Mike Quigley
#
# It seems likely that more of these daily puzzles will involve Intcode.
# This file will be maintained as the latest version of my Intcode emulator,
# in addition to daily snapshot files.
#
# 2019-12-07: Object-oriented, to enable multiple instances
#             Removed disassembler. That can be moved somewhere separate
# 2019-12-09: Relative memory addresses. Mode 2 means that the address
#             is added to a base value, which can be modified by opcode 9
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

class Intcomp:

    #mem is RAM size
    def __init__(self, mem):
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
                self.write(1, int(input("P> ")))
                self.pc += 2
            elif op == 4:
                print(self.fetch(1))
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
                print("END")
                halt = True
            else:
                print("ERROR UNKNOWN OPCODE", op, "AT ADDR", self.pc)
                halt = True

comp = Intcomp(4096)
inp = "Input String"
while inp != "EXIT":
    inp = input("> ")
    if inp == "LIST":
        comp.list()
    elif inp == "CLEAR":
        comp.clear()
    elif inp == "LOAD":
        comp.load(input("PROGRAM: "))
    elif inp == "LOADFILE":
        comp.loadfile(input("FILENAME: "))
    elif inp == "POKE":
        addr = int(input("ADDR: "))
        val = int(input("VAL: "))
        comp.ram[addr] = val
    elif inp == "RUN":
        comp.run()
