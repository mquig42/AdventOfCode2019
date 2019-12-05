###############################################################################
# AoC_2-1.py
# 2019-12-03
# Mike Quigley
#
# For description, see https://adventofcode.com/2019/day/2
# Basically, it simulates a small computer. So far, there are 3 opcodes,
# and each opcode takes 3 arguments, so each instruction takes 4 units of
# memory. All arguments are memory addresses, which are sequential from 0
#
# Instruction Set:
# 1: ADD a b dest: Adds a + b, stores result in dest
# 2: MUL a b dest: As above, but multiplies instead of adds
# 99: HALT
#
# Any opcode not in the list should throw an error and halt
###############################################################################

ram = []

def list():
    for i in range(0,len(ram),4):
        print(i, ':', ram[i:i+4])

def init(n):
    for i in range(0,n):
        ram.append(0)

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
            print("END")
            return
        else:
            print("ERROR UNKNOWN OPCODE", ram[i], "AT ADDR", i)
            return

init(128)
inp = "Input String"
while inp != "EXIT":
    inp = input("> ")
    if inp == "LIST":
        list()
    elif inp == "LOAD":
        load(input("PROGRAM: "))
    elif inp == "RUN":
        run()
