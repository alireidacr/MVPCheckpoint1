# simulation of ising model
# Alasdair Reid, s1539349

import numpy as np
import random as rnd
import math
import sys
from DataOut import DataOut

rnd.seed(0) # seed random number generator with interger, ensuring repeated performance throughout runs

# function to get systems parameters from command line
def getInputParams():
    dimensions = int(sys.argv[1]);
    temp = float(sys.argv[2]);
    dynamics = sys.argv[3];

    return dimensions, temp, dynamics

def randomSpins(dimensions):
    lattice = np.zeros((dimensions, dimensions))
    for loop in range(0, dimensions):
        for counter in range(0, dimensions):
            if (rnd.random() < 0.5):
                lattice[loop, counter] = -1
            else:
                lattice[loop, counter] = 1

    return lattice

def allignedSpins(dimensions):
    lattice = np.ones((dimensions, dimensions))
    return lattice


def getNearestNeighbours(pos, lattice):
    # function to determine nearest neighbours of given pos,
    # and enforce periodic boundary conditions
    nearestNeighbours = [] # list to contain tuples of nearest neighbours coordinates
    if (pos[1] == lattice.shape[1] -1):
        nearestNeighbours.append((pos[0], 0))
    else:
        nearestNeighbours.append((pos[0], pos[1] +1))
    if (pos[1] == 0):
        nearestNeighbours.append((pos[0], lattice.shape[1] -1))
    else:
        nearestNeighbours.append((pos[0], pos[1] -1))
    if (pos[0] == lattice.shape[1] -1):
        nearestNeighbours.append((0, pos[1]))
    else:
        nearestNeighbours.append((pos[0] +1, pos[1]))
    if (pos[0] == 0):
        nearestNeighbours.append((lattice.shape[1] -1, pos[1]))
    else:
        nearestNeighbours.append((pos[0] -1, pos[1]))

    return nearestNeighbours


def updateState(temp, lattice, dynamicsFunc):
    return dynamicsFunc(temp, lattice)

def updateStateGlauber(temp, lattice):
    pos = (rnd.randint(0, lattice.shape[1] -1), rnd.randint(0, lattice.shape[1] -1))

    energyChange = glauberEnergyChange(pos, lattice)
    if (metropolisFlip(energyChange, temp)):
        lattice[pos] = - lattice[pos]

    return lattice

def glauberEnergyChange(pos, lattice):
    nearestNeighbours = getNearestNeighbours(pos, lattice)

    # determine spins of nearest neighbours by list comprehension
    NNSpin = [lattice[NN] for NN in nearestNeighbours]

    energyChange = 2 * lattice[pos] * sum(NNSpin)
    return energyChange

def updateSateKawasaki(temp, lattice):
    pos1 = (rnd.randint(0, lattice.shape[1] -1), rnd.randint(0, lattice.shape[1] -1))
    pos2 = (rnd.randint(0, lattice.shape[1] -1), rnd.randint(0, lattice.shape[1] -1))

    while (pos1 == pos2): # ensure same spin has not been selected twice
        pos2 = (rnd.randint(0, lattice.shape[1] -1), rnd.randint(0, lattice.shape[1] -1))

    energyChange = kawasakiEnergyChange(pos1, pos2, lattice)

    if (metropolisFlip(energyChange, temp)):
        old1 = lattice[pos1]
        lattice[pos1] = lattice[pos2]
        lattice[pos2] = old1

    return lattice

def kawasakiEnergyChange(pos1, pos2, lattice):
    spin1 = lattice[pos1]
    spin2 = lattice[pos2]

    NN1 = getNearestNeighbours(pos1, lattice)
    NN2 = getNearestNeighbours(pos2, lattice)

    if (spin1 == spin2):
        return 0

    elif (pos2 in NN1):
        # return energy change for each spin swap, not including the interaction with the other swapped spin
        NNSpin1 = [lattice[NN] for NN in NN1]
        NNSpin2 = [lattice[NN] for NN in NN2]

        energyChange1 = 2 * lattice[pos1] * (sum(NNSpin1 - lattice[pos2]))
        energyChange2 = 2 * lattice[pos2] * (sum(NNSpin2 - lattice[pos1]))

        return energyChange1 + energyChange2

    else:
        # chosen spins are not nearest neighbours
        NNSpin1 = [lattice[NN] for NN in NN1]
        NNSpin2 = [lattice[NN] for NN in NN2]

        energyChange1 = 2 * lattice[pos1]* sum(NNSpin1)
        energyChange2 = 2 * lattice[pos2]* sum(NNSpin2)

        return energyChange1 + energyChange2


def metropolisFlip(energyChange, temp):
    if (energyChange < 0):
        return True
    elif (rnd.random() < math.exp(- energyChange / temp)):
        return True
    else:
        return False

def systemEnergy(lattice):
    # calculates the total energy of the system in it's current state
    energy = 0
    for i in range(lattice.shape[1]):
        for j in range(lattice.shape[1]):
            NNs = getNearestNeighbours((i, j), lattice)
            energy -= sum([lattice[(i, j)] * lattice[NN] for NN in NNs])

    return energy/2 # must divide by two to take into account double counting of pairs



def main():
    dimensions, temp, dynamics = getInputParams()

    lattice = randomSpins(dimensions) # initialise array to store spin values
    #lattice = allignedSpins(dimensions)

    # initialise output class instance
    output = DataOut(dimensions)

    if (dynamics.lower() == "glauber"):
        dynamicsFunc = updateStateGlauber
    else:
        # define updateState function for Kawasaki dynamics
        dynamicsFunc = updateSateKawasaki

    for temp in np.linspace(0.5, 50, 20): # remove this line to allow editing of temp and dynamics at command line
        sweeps = 0
        magData = []
        EData = []
        while sweeps < 10000:
            counter = 0
            while counter < (dimensions**2):
                lattice = updateState(temp, lattice, dynamicsFunc)
                counter += 1
            """
            if (sweeps%10 == 0):
                output.formatOutputMatrix(lattice)
                print ("sweep: %5d" % (sweeps))
            """
            if (sweeps > 100 and sweeps%10 == 0):
                magData.append(np.sum(lattice))
                EData.append(systemEnergy(lattice))

            sweeps += 1

        output.recordMagData(temp, magData, dynamics)
        output.recordEnergyData(temp, EData, dynamics)

        # at end of temperature run, calculate suscebtibility of the system, and write to file along with temperature
        # also implement measurement of total energy of the system

        #np.savetxt("output.txt", lattice)



main()
