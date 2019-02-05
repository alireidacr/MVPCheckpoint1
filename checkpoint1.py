# simulation of ising model
# Alasdair Reid, s1539349

import numpy as np
import random as rnd
import math
from os import system
import sys

rnd.seed(0) # seed random number generator with interger, ensuring repeated performance throughout runs

# function to get systems parameters from command line
def getInputParams():
    dimensions = int(sys.argv[1]);
    temp = int(sys.argv[2]);
    dynamics = sys.argv[3];

    return dimensions, temp, dynamics

def randomSpins(dimensions):
    lattice = np.zeros((dimensions, dimensions))
    for loop in range(0, dimensions - 1):
        for counter in range(0, dimensions - 1):
            if (rnd.random() < 0.5):
                lattice[loop, counter] = -1
            else:
                lattice[loop, counter] = 1

    return lattice


def getNearestNeighbours(pos, dimensions, lattice):
    # function to determine nearest neighbours of given pos,
    # and enforce periodic boundary conditions
    nearestNeighbours = [] # list to contain tuples of nearest neighbours coordinates
    if (pos[1] == dimensions -1):
        nearestNeighbours.append((pos[0], 0))
    else:
        nearestNeighbours.append((pos[0], pos[1] +1))
    if (pos[1] == 0):
        nearestNeighbours.append((pos[0], dimensions -1))
    else:
        nearestNeighbours.append((pos[0], pos[1] -1))
    if (pos[0] == dimensions -1):
        nearestNeighbours.append((0, pos[1]))
    else:
        nearestNeighbours.append((pos[0] +1, pos[1]))
    if (pos[0] == 0):
        nearestNeighbours.append((dimensions -1, pos[1]))
    else:
        nearestNeighbours.append((pos[0] -1, pos[1]))

    return nearestNeighbours

def glauberEnergyChange(pos, dimensions, lattice):
    nearestNeighbours = getNearestNeighbours(pos, dimensions, lattice)

    # determine spins of nearest neighbours by list comprehension
    NNSpin = [lattice[NN[0], NN[1]] for NN in nearestNeighbours]

    energyChange = 2 * lattice[pos[0], pos[1]] * sum(NNSpin)
    return energyChange

def kawasakiEnergyChange(pos1, pos2, dimensions, lattice):
    spin1 = lattice[pos1[0], pos1[1]]
    spin2 = lattice[pos2[0], pos2[1]]

    NN1 = getNearestNeighbours(pos1, dimensions, lattice)
    NN2 = getNearestNeighbours(pos2, dimensions, lattice)

    if (spin1 == spin2):
        return 0

    elif (pos2 in NN1):
        # return energy change for each spin swap, not including the interaction with the other swapped spin
        NNSpin1 = [lattice[NN[0], NN[1]] for NN in NN1]
        NNSpin2 = [lattice[NN[0], NN[1]] for NN in NN2]

        energyChange1 = 2 * lattice[pos1[0], pos1[1]] * (sum(NNSpin1 - lattice[pos2[0], pos2[1]]))
        energyChange2 = 2 * lattice[pos2[0], pos2[1]] * (sum(NNSpin2 - lattice[pos1[0], pos2[1]]))

        return energyChange1 + energyChange2

    else:
        # chosen spins are not nearest neighbours
        NNSpin1 = [lattice[NN[0], NN[1]] for NN in NN1]
        NNSpin2 = [lattice[NN[0], NN[1]] for NN in NN2]
        
        energyChange1 = 2 * lattice[pos1[0], pos1[1]] * sum(NNSpin1)
        energyChange2 = 2 * lattice[pos2[0], pos2[1]] * sum(NNSpin2)

        return energyChange1 + energyChange2

def updateStateGlauber(dimensions, temp, lattice):
    pos = (rnd.randint(0, dimensions - 1), rnd.randint(0, dimensions -1))

    energyChange = glauberEnergyChange(pos, dimensions, lattice)
    if (metropolisFlip(energyChange, temp)):
        lattice[pos[0], pos[1]] = - lattice[pos[0], pos[1]]

    return lattice

def updateSateKawasaki(dimensions, temp, lattice):
    pos1 = (rnd.randint(0, dimensions -1), rnd.randint(0, dimensions -1))
    pos2 = (rnd.randint(0, dimensions -1), rnd.randint(0, dimensions -1))

    energyChange = kawasakiEnergyChange(pos1, pos2, dimensions, lattice)
    if (metropolisFlip(energyChange, temp)):
        old1 = lattice[pos1[0], pos1[1]]
        lattice[pos1[0], pos1[1]] = lattice[pos2[0], pos2[1]]
        lattice[pos2[0], pos2[1]] = old1

    return lattice

def updateState(dimensions, temp, lattice, dynamicsFunc):
    return dynamicsFunc(dimensions, temp, lattice)

def metropolisFlip(energyChange, temp):
    if (energyChange < 0):
        return True
    elif (rnd.random() < math.exp(- energyChange / temp)):
        return True
    else:
        return False


def formatOutputMatrix(lattice):
    # format output file as x y spin(x, y)
    file = open("output.txt", "w")
    for i in range(lattice.shape[1]-1):
        for j in range(lattice.shape[1]-1):

            file.write(str(i) + " "  + str(j) + " " + str(lattice[i, j]) + "\n")
    file.close()


def main():
    dimensions, temp, dynamics = getInputParams()
    lattice = randomSpins(dimensions) # initialise array to store spin values

    if (dynamics.lower() == "glauber"):
        dynamicsFunc = updateStateGlauber
    else:
        # define updateState function for Kawasaki dynamics
        dynamicsFunc = updateSateKawasaki

    for temp in range(1, 201, 10):
        sweeps = 0
        magData = []
        while sweeps < 10000:
            counter = 0
            while counter < (dimensions**2):
                lattice = updateState(dimensions, temp, lattice, dynamicsFunc)
                counter += 1
            sweeps += 1

            if (sweeps%10 == 0):
                formatOutputMatrix(lattice)

            print ("sweep: %5d" % (sweeps))

            if (sweeps > 100 and sweeps%10 == 0):
                magData.append(np.sum(lattice))

        # at end of temperature run, calculate suscebtibility of the system, and write to file along with temperature
        # also implement measurement of total energy of the system

        #np.savetxt("output.txt", lattice)



main()
