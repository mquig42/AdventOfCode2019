################################################################################
# AoC_23-2b.py
# 2019-12-27
# Mike Quigley
#
# https://adventofcode.com/2019/day/23
#
# Simulates network of 50 Intcode machines communicating with each other
# Try simpler network model, using a main loop and message queue instead of
# 50 different threads. Also don't use prompt_for_input, instead always put
# any available input on inQ, and check if outQ is empty before reading.
################################################################################
import INTCODE_T
import queue
import time

#Init and start Intcode threads
comps = [INTCODE_T.Intcomp_T(i,'CPU'+str(i),4096) for i in range(50)]
for c in comps:
    c.loadfile('NIC')
    c.start()
    c.inQ.put(c.threadID)
    c.inQ.put(-1)

#Message queues and NAT packet
messageQ = [queue.Queue() for i in range(50)]
natpack = (0,0)

#Main loop
while True:
    for i in range(len(comps)):
        #Add any available packets to inQ
        while not messageQ[i].empty():
            pkt = messageQ[i].get()
            comps[i].inQ.put(pkt[0])
            comps[i].inQ.put(pkt[1])
        #Read any output packets and route them to the correct message queue
        while not comps[i].outQ.empty():
            dest = comps[i].outQ.get()
            if dest == 255:
                natpack = (comps[i].outQ.get(), comps[i].outQ.get())
            else:
                messageQ[dest].put((comps[i].outQ.get(), comps[i].outQ.get()))

    #Let Intcode threads process their packets
    time.sleep(0.5)

    #Check all message and output queues to see if they're all empty
    all_empty = True
    for q in messageQ:
        if not q.empty():
            all_empty = False
    for c in comps:
        if not c.outQ.empty():
            all_empty = False

    #If every queue is empty, the network is idle. Have the NAT send its packet
    if all_empty:
        print(natpack[1])
        comps[0].inQ.put(natpack[0])
        comps[0].inQ.put(natpack[1])


