################################################################################
# AoC_12-1.py
# 2019-12-12
# Mike Quigley
#
# https://adventofcode.com/2019/day/12
#
# Use a simplified physics model to calculate movements of 4 moons
# Each has position and velocity in 3 dimensions
# Velocity is per time step
# Gravity is evaluated separately on each axis, and just increments v by 1
#
# Energy is the sum of all position and velocity values
# Find total energy after 1000 time steps
################################################################################

class moon:
    def __init__(self, name, x, y, z):
        self.name = name
        self.pos = {'X': x, 'Y': y, 'Z': z}
        self.vel = {'X': 0, 'Y': 0, 'Z': 0}

    #Returns total energy
    def energy(self):
        potential = abs(self.pos['X']) + abs(self.pos['Y']) + abs(self.pos['Z'])
        kinetic = abs(self.vel['X']) + abs(self.vel['Y']) + abs(self.vel['Z'])
        return kinetic * potential

    #Adjust THIS moon's velocity based on position of another moon
    def applygravity(self, other):
        for axis in self.pos.keys():
            if self.pos[axis] < other.pos[axis]:
                self.vel[axis] += 1
            elif self.pos[axis] > other.pos[axis]:
                self.vel[axis] -= 1

    #Simulate one timestep of movement
    def move(self):
        for axis in self.pos.keys():
            self.pos[axis] += self.vel[axis]

    #prints a string describing the pos and vel of this moon
    def pr(self):
        print(self.name, self.pos, self.vel)

moons = []
moons.append(moon("Io", 1, 3, -11))
moons.append(moon("Europa", 17, -10, -8))
moons.append(moon("Ganymede", -1, -15, 2))
moons.append(moon("Callisto", 12, -4, -4))

for time in range(1000):
    for moonA in moons:
        for moonB in moons:
            moonA.applygravity(moonB)
    for moon in moons:
        moon.move()

e = 0
for moon in moons:
    e += moon.energy()
print(e)
