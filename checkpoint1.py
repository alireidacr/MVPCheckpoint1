# simulation of ising model
# Alasdair Reid, s1539349

import numpy as np
import random as rnd
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from os import system

rnd.seed(0) # seed random number generator with interger, ensuring repeated performance throughout runs

# function to get systems parameters from command line
def getInputParams():
    dimensions = int(input("Enter the side length of the Square Lattice: "))
    temp = float(input("Enter the system temperature: "))

    validDynamics = False
    while validDynamics == False:
        dynamics = input("Enter the system dynamics (Glauber/Kawasaki): ")
        if (dynamics.lower() != "glauber" and dynamics.lower() != "kawasaki"):
            print("Invalid input")
            print(dynamics)
        else:
            validDynamics = True
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
    energyChange = -2 * lattice[xPos, yPos] * np.sum(nearestNeighbours)
    return energyChange

def metropolisFlip(energyChange, temp):
    if (energyChange < 0):
        return True
    elif (rnd.random() < math.exp(- energyChange / temp)):
        return True
    else:
        return False


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


    counter = 0
    while counter < 10000:

        lattice = updateState(dimensions, lattice)
        np.savetxt("output.dat", lattice)

        counter += 1
        print(counter)

        # some measurement and animation code here

system('gnuplot isingAnimation.gnuplot &')
main()
