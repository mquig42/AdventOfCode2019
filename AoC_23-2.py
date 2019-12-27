################################################################################
# AoC_23-2.py
# 2019-12-27
# Mike Quigley
#
# https://adventofcode.com/2019/day/23
#
# Simulates network of 50 Intcode machines communicating with each other
# This problem is timing-sensitive. Program produces a wide variety of
# incorrect answers rather than a single correct one.
################################################################################
import threading
import queue
import INTCODE_T

network = dict()
idle = [0 for i in range(50)]

class nic(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = 'NIC' + str(threadID)
        self.compy = INTCODE_T.Intcomp_T(threadID + 50, 'COMP'+str(threadID), 4096, prompt_for_input=True)
        self.compy.loadfile('NIC')
        self.inQ = queue.Queue()

    def run(self):
        self.compy.start()
        self.compy.outQ.get()
        self.compy.inQ.put(self.threadID)

        while True:
            out = self.compy.outQ.get()
            if out == 'P>':
                #Request packet
                if self.inQ.empty():
                    idle[self.threadID] = 1
                    self.compy.inQ.put(-1)
                else:
                    packet = self.inQ.get()
                    self.compy.inQ.put(packet[0])
                    self.compy.inQ.put(packet[1])
            elif out == 'END':
                #Program ended
                break
            else:
                #Send packet
                x = self.compy.outQ.get()
                y = self.compy.outQ.get()
                if out != 255:
                    network[out].inQ.put((x,y))
                    idle[out] = 0
                else:
                    network[out].inp = (x,y)

class nat(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = 'NIC255'
        self.inp = (0,0)

    def run(self):
        while True:
            if sum(idle) == 50:
                if self.inp != (0,0):
                    print(self.inp[1])
                    network[0].inQ.put(self.inp)
                    idle[0] = 0

network[255] = nat(255)

for i in range(50):
    network[i] = nic(i)
for i in range(50):
    network[i].start()
network[255].start()
