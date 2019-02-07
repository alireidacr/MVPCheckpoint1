# class to contain data output methods for ising model simulation
import random as rnd
import math

class DataOut:

    def __init__(self, dimensions):
        self.dimensions = dimensions

    def formatOutputMatrix(self, lattice):
        # format output file as x y spin(x, y)
        file = open("output.txt", "w")
        for i in range(lattice.shape[1]):
            for j in range(lattice.shape[1]):
                file.write(str(i) + " "  + str(j) + " " + str(lattice[i, j]) + "\n")
        file.close()


    def findChi(self, temp, magData):
        magMean = sum(magData)/len(magData)
        magSquared = [mag**2 for mag in magData]

        chi = (1/(self.dimensions**2 * temp)) * ((sum(magSquared)/len(magSquared)) - magMean**2)

        return chi


    def findSpecHeat(self, temp, EData):
        EMean = sum(EData)/len(EData)
        ESquared = [E**2 for E in EData]

        specHeat = (1/(self.dimensions**2 * (temp**2))) * (sum(ESquared)/len(ESquared) - EMean**2)

        return specHeat


    def recordMagData(self, temp, magData, dynamics):
        magMean = sum(magData)/len(magData)
        chi = self.findChi(temp, magData)

        outputMag = "Data/magnetisation" + dynamics.upper() + ".txt"
        outputSus = "Data/susceptibility" + dynamics.upper() + ".txt"
        self.appendToFile(outputMag, temp, abs(magMean))
        self.appendToFile(outputSus, temp, chi)


    def recordEnergyData(self, temp, EData, dynamics):
        EMean = sum(EData)/len(EData)
        specHeat = self.findSpecHeat(temp, EData)
        specHeatError = self.bootstrapError(temp, EData, 20, self.findSpecHeat)

        outputEnergy = "Data/energy" + dynamics.upper() + ".txt"
        outputSpec = "Data/specHeat" + dynamics.upper() + ".txt"
        self.appendToFile(outputEnergy, temp, EMean)
        self.appendToFile(outputSpec, temp, specHeat, specHeatError)


    def appendToFile(self, file, xVal, yVal, error=""):
        file = open(file, "a+")
        file.write(str(xVal) + " " + str(yVal) + " " + str(error) + "\n")
        file.close()


    def bootstrapError(self, temp, dataSet, repeats, func='findSpecHeat'):
        vals = []
        for _ in range(repeats):
            resampleSet = []
            for _ in dataSet:
                resampleSet.append(rnd.choice(dataSet))
            vals.append(func(temp, resampleSet))

        valMean = sum(vals)/len(vals)
        valSquares = [val**2 for val in vals]
        valSquaresMean = sum(valSquares)/len(valSquares)

        return math.sqrt(valSquaresMean - (valMean**2))
