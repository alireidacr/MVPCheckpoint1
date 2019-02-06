# class to contain data output methods for ising model simulation

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

    def recordMagData(self, temp, magData):
        magMean = sum(magData)/len(magData)
        magSquared = [mag**2 for mag in magData]

        chi = (1/(self.dimensions**2 * temp)) * ((sum(magSquared)/len(magSquared)) - magMean**2)

        file = open("magnetisation.txt", "a+")
        file.write(str(temp) + " " + str(magMean) + "\n")
        file.close()

        file = open("susceptibility.txt", "a+")
        file.write(str(temp) + " " + str(chi) + "\n")
        file.close()

    def recordEnergyData(self, temp, EData):
        return 0
