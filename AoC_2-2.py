###############################################################################
# AoC_2-2.py
# 2019-12-03
# Mike Quigley
#
# For description, see https://adventofcode.com/2019/day/2#part2
# This uses the same computer as part 1, but tries to find which inputs produce
# a desired output. I'll try running the same program repeatedly.
###############################################################################

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

def run():
    for i in range(0, len(ram), 4):
        if ram[i] == 1:
            ram[ram[i+3]] = ram[ram[i+1]] + ram[ram[i+2]]
        elif ram[i] == 2:
            ram[ram[i+3]] = ram[ram[i+1]] * ram[ram[i+2]]
        elif ram[i] == 99:
            return
        else:
            print("ERROR UNKNOWN OPCODE", ram[i], "AT ADDR", i)
            return

def search():
    proGravAssist = "1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,13,1,19,1,5,19,23,2,10,23,27,1,27,5,31,2,9,31,35,1,35,5,39,2,6,39,43,1,43,5,47,2,47,10,51,2,51,6,55,1,5,55,59,2,10,59,63,1,63,6,67,2,67,6,71,1,71,5,75,1,13,75,79,1,6,79,83,2,83,13,87,1,87,6,91,1,10,91,95,1,95,9,99,2,99,13,103,1,103,6,107,2,107,6,111,1,111,2,115,1,115,13,0,99,2,0,14,0"
    for a in range(0,99):
        for b in range(0,99):
            clear()
            load(proGravAssist)
            ram[1] = a
            ram[2] = b
            run()
            if ram[0] == 19690720:
                return a,b

init(128)
inp = "Input String"
while inp != "EXIT":
    inp = input("> ")
    if inp == "LIST":
        list()
    elif inp == "CLEAR":
        clear()
    elif inp == "LOAD":
        load(input("PROGRAM: "))
    elif inp == "LOADNV":
        load(input("PROGRAM: "))
        ram[1] = int(input("NOUN: "))
        ram[2] = int(input("VERB: "))
        run()
        print(ram[0])
    elif inp == "RUN":
        run()
    elif inp == "SEARCH":
        print(search())
