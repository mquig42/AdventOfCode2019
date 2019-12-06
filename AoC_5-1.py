################################################################################
# AoC_5-1.py
# 2019-12-05
# Mike Quigley
#
# https://adventofcode.com/2019/day/5
#
# This is an intcode emulator, like day 2.
# The following features have been added:
#  *Parameter modes
#    Opcodes are treated as 5 digit numbers. Leading 0s are assumed.
#    The last two digits are the opcode. The remaining 3 determine if the
#    parameters are treated as values (1 for immediate mode),
#    or pointers (0 for position mode). It's right to left, so the first
#    digit refers to the third parameter.
#    Parameters that an instruction writes to must be in position mode
#  *New opcodes for input/output. These have only one parameter, not 3
#
# Opcode table:
#  1: ADD A B DEST - Adds A + B, result in DEST.
#  2: MUL A B DEST - Multiplies A * B, result in DEST
#  3: INP DEST     - Reads keyboard input to DEST
#  4: OUT A        - Print A
# 99: HALT
################################################################################

ram = []

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

def fetch(val, mode):
    if mode == 0:
        return ram[ram[val]]
    else:
        return ram[val]

def run():
    halt = False
    pc = 0
    op = 0
    pM = [0, 0, 0]
    while not halt:
        op = ram[pc] % 100
        pM[0] = (ram[pc] // 100) % 10
        pM[1] = (ram[pc] // 1000) % 10
        pM[2] = (ram[pc] // 10000) % 10
        if op == 1:
            ram[ram[pc+3]] = fetch(pc + 1, pM[0]) + fetch(pc + 2, pM[1])
            pc += 4
        elif op == 2:
            ram[ram[pc+3]] = fetch(pc + 1, pM[0]) * fetch(pc + 2, pM[1])
            pc += 4
        elif op == 3:
            ram[ram[pc+1]] = int(input("P> "))
            pc += 2
        elif op == 4:
            print(fetch(pc + 1, pM[0]))
            pc += 2
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
