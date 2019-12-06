################################################################################
# INTCODE.py
# 2019-12-05
# Mike Quigley
#
# It seems likely that more of these daily puzzles will involve Intcode.
# This file will be maintained as the latest version of my Intcode emulator,
# in addition to daily snapshot files.
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

ram = []
pM = [0, 0, 0]  #Parameter mode flags

#Dumps memory to screen
def list():
    for i in range(0,len(ram),4):
        print("{0:4d}: {1}".format(i,ram[i:i+4]))

#Used by listasm to display parameter mode flags
def flag(x):
    if x == 0:
        return "*"
    else:
        return " "

#Lists currently loaded program in assembly language
#This is not required by any puzzle, I just have a strange idea of fun
#Since instructions are variable length, this may work incorrectly
#for programs that rely on self-modification
def listasm():
    pc = 0
    op = 0
    while pc < len(ram):
        op = ram[pc] % 100
        pM[0] = (ram[pc] // 100) % 10
        pM[1] = (ram[pc] // 1000) % 10
        pM[2] = (ram[pc] // 10000) % 10
        if op == 1:
            #ram[ram[pc+3]] = fetch(pc, 1) + fetch(pc, 2)
            print("{0:4d}: ADD {2:8d}{1} {4:8d}{3} {5:8d}*"
                  .format(pc,flag(pM[0]),ram[pc+1],flag(pM[1]),ram[pc+2],ram[pc+3]))
            pc += 4
        elif op == 2:
            #ram[ram[pc+3]] = fetch(pc, 1) * fetch(pc, 2)
            print("{0:4d}: MUL {2:8d}{1} {4:8d}{3} {5:8d}*"
                  .format(pc,flag(pM[0]),ram[pc+1],flag(pM[1]),ram[pc+2],ram[pc+3]))
            pc += 4
        elif op == 3:
            #ram[ram[pc+1]] = int(input("P> "))
            print("{0:4d}: INP {1:8d}*".format(pc,ram[pc+1]))
            pc += 2
        elif op == 4:
            #print(fetch(pc, 1))
            print("{0:4d}: OUT {2:8d}{1}".format(pc,flag(pM[0]),ram[pc+1]))
            pc += 2
        elif op == 5:
            #pc = fetch(pc, 2) if fetch(pc, 1) != 0 else pc + 3
            print("{0:4d}: JNZ {2:8d}{1} {4:8d}{3}"
                  .format(pc,flag(pM[0]),ram[pc+1],flag(pM[1]),ram[pc+2]))
            pc += 3
        elif op == 6:
            #pc = fetch(pc, 2) if fetch(pc, 1) == 0 else pc + 3
            print("{0:4d}: JEZ {2:8d}{1} {4:8d}{3}"
                  .format(pc,flag(pM[0]),ram[pc+1],flag(pM[1]),ram[pc+2]))
            pc += 3
        elif op == 7:
            #ram[ram[pc+3]] = 1 if fetch(pc, 1) < fetch(pc, 2) else 0
            print("{0:4d}: TLT {2:8d}{1} {4:8d}{3} {5:8d}*"
                  .format(pc,flag(pM[0]),ram[pc+1],flag(pM[1]),ram[pc+2],ram[pc+3]))
            pc += 4
        elif op == 8:
            #ram[ram[pc+3]] = 1 if fetch(pc, 1) == fetch(pc, 2) else 0
            print("{0:4d}: TEQ {2:8d}{1} {4:8d}{3} {5:8d}*"
                  .format(pc,flag(pM[0]),ram[pc+1],flag(pM[1]),ram[pc+2],ram[pc+3]))
            pc += 4
        elif op == 99:
            print("{0:4d}: HALT".format(pc))
            pc += 1
        elif op == 0:
            print("{0:4d}: ZZZ {2:8d}{1} {4:8d}{3} {5:8d}*"
                  .format(pc,flag(pM[0]),ram[pc+1],flag(pM[1]),ram[pc+2],ram[pc+3]))
            pc += 4
        else:
            print("{0:4d}: {1}".format(pc,ram[pc]))
            pc += 1

#Generates list of 0s of length n, to serve as main memory for Intcode programs
def init(n):
    for i in range(0,n):
        ram.append(0)

#Sets all memory to 0
def clear():
    for i in range(0,len(ram)):
        ram[i] = 0

#Load program from console
def load(program):
    pL = program.split(',')
    for i in range(0,len(pL)):
        ram[i] = int(pL[i])

#Load program from file
def loadfile(filename):
    file = open(filename,'r')
    load(file.readline())
    file.close()

#Fetch value from RAM. Will dereference pointers if mode flag is 0
def fetch(pc, param):
    if pM[param - 1] == 0:
        return ram[ram[pc + param]]
    else:
        return ram[pc + param]

#Run program
def run():
    halt = False
    pc = 0
    op = 0
    while not halt:
        op = ram[pc] % 100
        pM[0] = (ram[pc] // 100) % 10
        pM[1] = (ram[pc] // 1000) % 10
        pM[2] = (ram[pc] // 10000) % 10
        if op == 1:
            ram[ram[pc+3]] = fetch(pc, 1) + fetch(pc, 2)
            pc += 4
        elif op == 2:
            ram[ram[pc+3]] = fetch(pc, 1) * fetch(pc, 2)
            pc += 4
        elif op == 3:
            ram[ram[pc+1]] = int(input("P> "))
            pc += 2
        elif op == 4:
            print(fetch(pc, 1))
            pc += 2
        elif op == 5:
            pc = fetch(pc, 2) if fetch(pc, 1) != 0 else pc + 3
        elif op == 6:
            pc = fetch(pc, 2) if fetch(pc, 1) == 0 else pc + 3
        elif op == 7:
            ram[ram[pc+3]] = 1 if fetch(pc, 1) < fetch(pc, 2) else 0
            pc += 4
        elif op == 8:
            ram[ram[pc+3]] = 1 if fetch(pc, 1) == fetch(pc, 2) else 0
            pc += 4
        elif op == 99:
            print("END")
            halt = True
        else:
            print("ERROR UNKNOWN OPCODE", op, "AT ADDR", pc)
            halt = True

init(1024)
inp = "Input String"
while inp != "EXIT":
    inp = input("> ")
    if inp == "LIST":
        list()
    elif inp == "CLEAR":
        clear()
    elif inp == "LOAD":
        load(input("PROGRAM: "))
    elif inp == "LOADFILE":
        loadfile(input("FILENAME: "))
    elif inp == "RUN":
        run()
    elif inp == "LISTASM":
        listasm()
