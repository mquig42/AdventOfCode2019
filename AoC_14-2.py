################################################################################
# AoC_14-1.py
# 2019-12-14
# Mike Quigley
#
# https://adventofcode.com/2019/day/14
#
# Today's input is a list of chemical reactions. For example:
# 2 TKWH, 5 NCMQC, 9 GRXH => 3 HPSK
# requires 2 TKWH, 5 NCMQC, 9 GRXH, and produces 3 HPSK
#
# Each reaction has one product (though usually multiple units of it)
# and each product has only a single reaction which produces it.
# This means that there is only one possible chain of reactions for any product
#
# Find out how much fuel can be made from 1000000000000 units of ore
################################################################################
import math
import time

class reaction:
    #Inits a reaction object from the description string in today's file
    def __init__(self, desc):
        p = desc.split('=>')[1].split()
        self.product = p[1]
        self.qty = int(p[0])
        self.inputs = dict()
        reactantlist = desc.split('=>')[0].split(',')
        for r in reactantlist:
            rs = r.split()
            self.inputs[rs[1]] = int(rs[0])

#Returns number of reactions required to produce p from ore (longest chain)
def steps_to_ore(product, reactions):
    #Trivial case: p comes from ore directly
    if product == 'ORE':
        return 0
    if 'ORE' in reactions[product].inputs:
        return 1
    #Otherwise find which input requires the most steps
    steps = [steps_to_ore(p, reactions) + 1 for p in reactions[product].inputs]
    return max(steps)

#Returns input with longest chain of reactions
def maxinput(inputlist, reactions):
    maxproduct = ''
    maxproduct_n = 0
    for i in inputlist:
        s = steps_to_ore(i, reactions)
        if s > maxproduct_n:
            maxproduct_n = s
            maxproduct = i
    return maxproduct

#Returns inputs required for a given amount of product
def quantify_inputs(qty, product, reactions):
    multiplier = math.ceil(qty / reactions[product].qty)
    r = dict()
    for k in reactions[product].inputs.keys():
        r[k] = reactions[product].inputs[k] * multiplier
    return r

#adds any chemicals in newlist to mainlist
def merge_inputs(mainlist, newlist):
    for n in newlist:
        if n in mainlist:
            mainlist[n] += newlist[n]
        else:
            mainlist[n] = newlist[n]

#Returns amount of ore required for n fuel
def ore_for_fuel(n, reactions):
    fuelinputs = quantify_inputs(n, 'FUEL', reactions)

    while len(fuelinputs) > 1:
        m = maxinput(fuelinputs, reactions)
        q = fuelinputs[m]
        del fuelinputs[m]
        merge_inputs(fuelinputs, quantify_inputs(q, m, reactions))

    return fuelinputs['ORE']

start_time = time.time()
reactions = dict()
file = open('AoC_14.txt','r')
for line in file:
    r = reaction(line)
    reactions[r.product] = r
file.close()

#Comb search. Start with step size of one million
step = 1000000
i = 0
while True:
    while True:
        ore = ore_for_fuel(i, reactions)
        if ore > 1000000000000:
            break
        i += step
    i -= step
    step = step // 2
    if step == 0:
        break
print(i)
print('Elapsed Time:', '{0:0.3f}s'.format(time.time() - start_time))
    
