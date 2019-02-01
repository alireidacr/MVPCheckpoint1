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

def getNearestNeighbours(xPos, yPos, dimensions, lattice):
    nearestNeighbours = np.zeros(4) # array to contain spins of nearest neighbours to position given as argument
    # chain of if statements to enforce periodic boundary conditions - find a more elegant way to do this
    if (yPos == dimensions - 1):
        nearestNeighbours[0] = lattice[xPos, 0]
    else:
        nearestNeighbours[0] = lattice[xPos, yPos + 1]
    if (yPos == 0):
        nearestNeighbours[1] = lattice[xPos, dimensions - 1]
    else:
        nearestNeighbours[1] = lattice[xPos, yPos - 1]
    if (xPos == dimensions - 1):
        nearestNeighbours[2] = lattice[0, yPos]
    else:
        nearestNeighbours[2] = lattice[xPos + 1, yPos]
    if (xPos == 0):
        nearestNeighbours[3] = lattice[dimensions - 1, yPos]
    else:
        nearestNeighbours[3] = lattice[xPos - 1, yPos]

    return nearestNeighbours

def glauberEnergyChange(xPos, yPos, dimensions, lattice):
    nearestNeighbours = getNearestNeighbours(xPos, yPos, dimensions, lattice)
    energyChange = 2 * lattice[xPos, yPos] * np.sum(nearestNeighbours)
    return energyChange

def metropolisFlip(energyChange, temp):
    if (energyChange < 0):
        return True
    elif (rnd.random() < math.exp(- energyChange / temp)):
        return True
    else:
        return False

def formatOutputMatrix(lattice):
    # format output file as x, y, spin(x, y) to avoid gnu plot loading error
    file = open("output.txt", "w")
    for i in range(lattice.shape[1]-1):
        for j in range(lattice.shape[1]-1):

            file.write(str(i) + " "  + str(j) + " " + str(lattice[i, j]) + "\n")
    file.close()


def main():
    dimensions, temp, dynamics = getInputParams()
    lattice = randomSpins(dimensions) # initialise array to store spin values

    if (dynamics.lower() == "glauber"):
        def updateState(dimensions, lattice):
            xPos = rnd.randint(0, dimensions - 1)
            yPos = rnd.randint(0, dimensions - 1)

            energyChange = glauberEnergyChange(xPos, yPos, dimensions, lattice)
            if (metropolisFlip(energyChange, temp)):
                lattice[xPos, yPos] = - lattice[xPos, yPos]

            return lattice
    else:
        def updateState(dimensions, lattice):
            return 0 # do nothing for the time being


    sweeps = 0
    while sweeps < 10000:
        counter = 0
        while counter < (dimensions**2):
            lattice = updateState(dimensions, lattice)
            counter += 1
        sweeps += 1
        formatOutputMatrix(lattice)

        #np.savetxt("output.txt", lattice)

        # some measurement and animation code here

main()
