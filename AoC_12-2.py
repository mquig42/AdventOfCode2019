################################################################################
# AoC_12-2.py
# 2019-12-12
# Mike Quigley
#
# https://adventofcode.com/2019/day/12#part2
#
# Use a simplified physics model to calculate movements of 4 moons
# Each has position and velocity in 3 dimensions
# Velocity is per time step
# Gravity is evaluated separately on each axis, and just increments v by 1
#
# Run until simulation state matches a previous state, then print # of timesteps
# WARNING: This will take a long time to run. I benchmarked it at 283 years.
# see part b for a faster solution
################################################################################

class moon:
    def __init__(self, name, x, y, z):
        self.name = name
        self.pos = [x,y,z]
        self.vel = [0,0,0]

    #Returns total energy
    def energy(self):
        potential = abs(self.pos[0]) + abs(self.pos[1]) + abs(self.pos[2])
        kinetic = abs(self.vel[0]) + abs(self.vel[1]) + abs(self.vel[2])
        return kinetic * potential

    #Adjust velocity of two moons based on their positions
    def applygravityboth(self, other):
        for i in range(len(self.pos)):
            if self.pos[i] != other.pos[i]:
                delta = (other.pos[i]-self.pos[i])//abs(other.pos[i]-self.pos[i])
                self.vel[i] += delta
                other.vel[i] -= delta
        

    #Simulate one timestep of movement
    def move(self):
        for i in range(len(self.pos)):
            self.pos[i] += self.vel[i]

    #prints a string describing the pos and vel of this moon
    def pr(self):
        print(self.name, self.pos, self.vel)

    #returns a string representing the current state of this moon
    def statestr(self):
        return "{0}{1}".format(self.pos, self.vel)

moons = []
moons.append(moon("Io", 1, 3, -11))
moons.append(moon("Europa", 17, -10, -8))
moons.append(moon("Ganymede", -1, -15, 2))
moons.append(moon("Callisto", 12, -4, -4))

states = set()
time = 0

while True:
    state = ""
    moons[0].applygravityboth(moons[1])
    moons[0].applygravityboth(moons[2])
    moons[0].applygravityboth(moons[3])
    moons[1].applygravityboth(moons[2])
    moons[1].applygravityboth(moons[3])
    moons[2].applygravityboth(moons[3])
    for moon in moons:
        moon.move()
        state += moon.statestr()
    if state in states:
        print("End time:", time)
        break
    states.add(state)
    time += 1
    if time % 1000000 == 0:
        print("Time:", time)

e = 0
for moon in moons:
    e += moon.energy()
print(e)
