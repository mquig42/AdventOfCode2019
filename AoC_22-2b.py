################################################################################
# AoC_22-2b.py
# 2019-12-30
# Mike Quigley
#
# Based on the following:
# https://codeforces.com/blog/entry/72593
#
# This program should help with math, and be able to solve both parts of day 22
################################################################################

#Reads the shuffle instructions file and returns a list of tuples
#representing the shuffles as (a,b) of f(x)=(a*x+b)%size
def readshuffles(filename):
    functions = []
    file = open(filename,'r')
    for line in file:
        line = line.strip()
        if line == 'deal into new stack':
            functions.append((-1,-1))
        elif line.startswith('cut'):
            n = int(line.replace('cut ',''))
            functions.append((1, n*-1))
        elif line.startswith('deal with'):
            n = int(line.replace('deal with increment ',''))
            functions.append((n,0))
    file.close()
    return functions

#Execute a shuffle operation
def exs(op, x, m):
    return (op[0]*x + op[1]) % m

#Execute all shuffles
def exall(ops, x, m):
    for op in ops:
        x = exs(op,x,m)
    return x

#Compose two tuples into one
def compose(a, b, m):
    return ((a[0]*b[0])%m, (a[1]*b[0]+b[1])%m)

#Compose entire shuffle instruction list into a single tuple
def composeall(functions, mod):
    while len(functions) > 1:
        functions[0] = compose(functions[0], functions.pop(1), mod)
    return functions[0]

#Apparently, Fermat came up with this
def inv(a, n):
    return pow(a, n-2, n)

#Solves part 1
def solvepart1(filename):
    card = 2019
    decksize = 10007
    return exs(composeall(readshuffles(filename), decksize), card, decksize)

#Solves part 2
def solvepart2(filename):
    slot = 2020
    m = 119315717514047
    k = 101741582076661
    F = composeall(readshuffles(filename), m)

    #Arcane sorcery. Even more mysterious than the rest of this program
    A = pow(F[0], k, m)
    B = (F[1]*(A-1) * inv(F[0]-1,m))%m
    Fk = (A, B)
    return ((slot - B) * inv(A, m)) % m

print('Part 1:', solvepart1('AoC_22.txt'))
print('Part 2:', solvepart2('AoC_22.txt'))
        
