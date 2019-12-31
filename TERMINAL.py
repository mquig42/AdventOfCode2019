################################################################################
# Terminal.py
# 2019-12-17
# Mike Quigley
#
# Terminal interface for Intcode thread
#
# This provides an ASCII terminal for Intcode programs.
# Initially, it supports the same commands as Intcode.py (LOADFILE, POKE, etc.)
# Once the Intcode program is running, any output will be treated as an ASCII
# value and printed to the screen. Numbers greater than 255 will be
# printed directly.
#
# Prompt_for_input mode is enabled. The input prompt is displayed as 'P>'
# Input will be fed to the queue as individual ASCII values
#
# Useful for the second part of day 17
#
# Note: Because Python threads can't be restarted after they end,
#       Intcode programs can only be run once.
################################################################################
import INTCODE_T

def runterm(comp):
    comp.start()

    while True:
        outp = comp.outQ.get()
        if outp == 'END':
            print(outp)
            break
        elif outp == 'P>':
            inp = input('P> ')
            for c in inp:
                comp.inQ.put(ord(c))
                comp.outQ.get()
            comp.inQ.put(10)
        elif outp < 256:
            print(chr(outp),end='')
        else:
            print(outp)

comp = INTCODE_T.Intcomp_T(1,'comp',8192,prompt_for_input=True)
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
        runterm(comp)
