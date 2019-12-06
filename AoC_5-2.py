################################################################################
# AoC_5-2.py
# 2019-12-05
# Mike Quigley
#
# https://adventofcode.com/2019/day/5#part2
#
# Expands 5-1 with even more opcodes, for comparison and conditional jump
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

def list():
    for i in range(0,len(ram),4):
        print(i, ':', ram[i:i+4])

def init(n):
    for i in range(0,n):
        ram.append(0)

def clear():
    for i in range(0,len(ram)):
        ram[i] = 0

def load(program):
    pL = program.split(',')
    for i in range(0,len(pL)):
        ram[i] = int(pL[i])

def loadfile(filename):
    file = open(filename,'r')
    load(file.readline())
    file.close()

def fetch(pc, param):
    if pM[param - 1] == 0:
        return ram[ram[pc + param]]
    else:
        return ram[pc + param]

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
