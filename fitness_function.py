from math import floor, sqrt, ceil
import numpy as np
import scipy.interpolate
import scipy.stats as stats
import random, itertools
from copy import deepcopy

"""
Example usage:
solution = [2,2]
f = Fitness_Function(sphere_function, 0, 2)
fitness = f.evaluate(solution)
"""

MOD_SAMPLES = 103.0

def main():
    ff = Fitness_Function(sphere_function, 0, 2)
    ff.transform(-1)
    #print fitness2([1,1])
    #plotFitnessFunction(ff.fitness1)
    #plotFitnessFunction(ff.fitness2)
    #print ff.correlation()

def sphere_function(vals):
    total = 0.0
    for val in vals:
        total += val*val
    return total

def rosenbrock_function(vals, mods):
    total = 0.0
    for i in range(len(vals)-1):
        res = 100*(vals[i+1] - vals[i]**2)**2 + (vals[i]-1)**2

class Fitness_Function:
    def __init__(self, func, optimal, arglen):
        self.func = func
        self.fitness1 = func
        self.fitness2 = None
        self.optimal = 0
        self.arglen = arglen
        self.range_ = (-512, 512)
        self.flipped = False

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

    def setMods(self):
        dims = tuple([MOD_SAMPLES for i in range(self.arglen)])
        #self.mods = np.fromfunction(np.vectorize(self.random_mod), dims)
        self.mods = np.random.randn(*dims)*self.sd()*10*(1-abs(self.corr))
    
    def get_mod(self, point):
        """
        points = []
        values = []
        for combo in itertools.product(range(len(self.mods)), range(len(self.mods))):
            points.append(combo)
            values.append(self.mods.item(combo))

        ix = []
        for combo in itertools.product(*point):
            ix.append(combo)
        print ix
        print np.shape(points), np.shape(values), np.shape(ix)
        return scipy.interpolate.griddata(points, self.mods, ix)
        """
        interval = float(self.range_[1] - self.range_[0])/MOD_SAMPLES
        opts = []
        for i in range(len(point)):
            opts.append([floor(point[i]), ceil(point[i])])
            if opts[i][1] >= MOD_SAMPLES :
                opts[i].pop(1)
            elif opts[i][0] < 0:
                opts[i].pop(0)
        
        points = []
        values = []
        for combo in itertools.product(*opts):
            points.append(combo)
            values.append(self.mods.item(combo))
    

        try: #various things could go wrong with interpolation
            return scipy.interpolate.griddata(points, values, tuple(point))
        except:
            return values[0]
        
    def random_mod(self, *vals):
        sd = self.sd()
        return random.normalvariate(0, 10*sd * (1 - abs(self.corr)))

    def switch_to_fitness2(self, corr):
        self.corr = corr
        self.setMods()
        fitness2 = self.create_alternate_fitness_function()
        if corr < 0:
            self.fitness2 = self.invert(fitness2)
        self.fitness2 = fitness2
        self.flipped = True

    def switch_to_fitness1(self):
        self.flipped = False

    def create_alternate_fitness_function(self):
        def fitness2(vals):
            original = self.fitness1(vals)
            #print "original", original
            #print "vals", vals
            #print "mods", self.mods[0][0]
            #print "get", self.get_mod(vals)
            interval = float(self.range_[1] - self.range_[0])/MOD_SAMPLES
            vals = [((self.range_[0]*-1)+i)/interval for i in vals]
          
            try:
                res = self.get_mod(vals)
                return original + self.get_mod(vals)
            except Exception as e:
                return original + self.mods
        return fitness2

    def invert(self, function):
        def inverted(vals):
            return function(vals) * -1
        return inverted

if __name__ == "__main__":
    main()
