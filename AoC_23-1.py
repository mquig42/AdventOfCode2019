################################################################################
# AoC_23-1.py
# 2019-12-27
# Mike Quigley
#
# https://adventofcode.com/2019/day/23
#
# Simulates network of 50 Intcode machines communicating with each other
################################################################################
import threading
import queue
import INTCODE_T

network = dict()

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
                network[out].inQ.put((x,y))

class nic255(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = 'NIC255'
        self.inQ = queue.Queue()

    def run(self):
        packet = self.inQ.get()
        print(packet[1])

network[255] = nic255(255)
network[255].start()

for i in range(50):
    network[i] = nic(i)
for i in range(50):
    network[i].start()
