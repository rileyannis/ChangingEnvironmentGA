from math import floor, sqrt
import numpy as np
import scipy.stats as stats
import random

"""
Example usage:
solution = [2,2]
f = Fitness_Function(sphere_function, 0, 2)
fitness = f.evaluate(solution)
"""

def main():
    ff = Fitness_Function(sphere_function, 0, 2)
    ff.transform(-1)
    #print fitness2([1,1])
    #plotFitnessFunction(ff.fitness1)
    #plotFitnessFunction(ff.fitness2)
    #print ff.correlation()

def sphere_function(val, mods):
    res =  val*val
    res = np.add(res, mods)
    return res

class Fitness_Function:
    def __init__(self, func, optimal, arglen):
        self.func = func
        self.fitness1 = None
        self.fitness2 = None
        self.optimal = 0
        self.arglen = arglen
        self.range_ = (-512, 512)
        self.flipped = False

        def fitness1(vals):
            total = 0.0
            for val in vals:
                total += self.func(val, 0)
            return total

        self.fitness1 = fitness1

    def evaluate(self, solution):
        if self.flipped:
            return self.fitness2(solution)
        return self.fitness1(solution)

    def correlation(self, samples=100):
        vals1 = []
        vals2 = []
        for i in range(samples):
            solution = []
            for j in range(self.arglen):
                solution.append(random.randrange(*self.range_))
            vals1.append(self.fitness1(solution))
            vals2.append(self.fitness2(solution))
        slope, intercept, r_value, p_value, std_err = stats.linregress(vals1, vals2)
        return r_value

    def sd(self, samples=100):
        vals = []
        for i in range(samples):
            solution = []
            for j in range(self.arglen):
                solution.append(random.randrange(*self.range_))
            vals.append(self.fitness1(solution))
        return stats.tstd(vals)

    def setMods(self, corr):
        self.mods = {}
        sd = self.sd()
        for i in range(self.range_[0], self.range_[1]):
            self.mods[i] = random.normalvariate(0, 10*sd * (1 - abs(corr)))

    def transform(self, corr):
        self.setMods(corr)
        fitness2 = self.create_alternate_fitness_function()
        if corr < 0:
            self.fitness2 = self.invert(fitness2)
        self.fitness2 = fitness2

    def create_alternate_fitness_function(self):
        def fitness2(vals):
            total = 0.0
            for i in range(len(vals)):
                try: #Handle meshgrid objects for visualization
                    mods = np.array([self.mods[int(vals[i][j][k])] for j in range(len(vals[i])) for k in range(len(vals[i][j]))])
                    mods = np.reshape(mods, (sqrt(len(mods)), sqrt(len(mods))))

                except: #handle normal solutions
                    mods = self.mods[int(vals[i])]
                t = self.func(vals[i], mods)
                total += t
            return total
        return fitness2

    def invert(self, function):
        def inverted(vals):
            return function(vals) * -1
        return inverted

if __name__ == "__main__":
    main()
