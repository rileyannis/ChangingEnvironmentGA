"""
Going to attempt to convert the real value vector org into a real value array org
SHOULD work at this point
"""
#import cython
#cython.boundscheck(False)
#cython.wraparound(False)

import numpy as np

import random
from math import sqrt

LENGTH = None
RANGE_MIN = None
RANGE_MAX = None
MUTATION_EFFECT_SIZE = None

class RealValueVectorOrg(object):
    """
    this is a class that represents organisms as a real value vector
    fitness is determined by calling the fitness fuction
    the length is determined at object creation
    """

    def __init__(self, genotype=None):
        if genotype is None:
            genotype = _create_random_genotype()
        else:
            genotype = np.asarray(genotype, dtype=np.float64)
        self.genotype = genotype

    def fitness(self, environment):
        return environment(self.genotype)

    def get_mutant(self):        
        return RealValueVectorOrg(_get_mutated_genotype(self.genotype, MUTATION_EFFECT_SIZE))

    def get_clone(self):
        return RealValueVectorOrg(self.genotype)

    def __eq__(self, other):
        return self.genotype == other.genotype

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "RealValueVectorOrg({})".format(self.genotype)

    def __repr__(self):
        return str(self)

    def is_better_than(self, other, environment):
        return self.fitness(environment) < other.fitness(environment)

    def distance(self, other, environment):
        dist = 0.0
        for i in range(self.genotype.shape[0]):
            dist += (self.genotype[i] - other.genotype[i])**2

        return sqrt(dist)

def _get_mutated_genotype(genotype, effect_size):
    "Mutates one locus in organism at random"
    mut_location = random.randrange(genotype.shape[0])
    delta = random.normalvariate(0, effect_size)
    mutant_value = genotype[mut_location] + delta
    #Assignement returns a copy
    mutant = np.array(genotype, copy=True)
    mutant[mut_location] = _wrap_around(mutant_value, RANGE_MIN, RANGE_MAX)            
    return mutant

def _wrap_around(value, min_, max_):
    width = max_ - min_
    while value < min_ or value > max_:
        if value < min_:
            value += width
        else:
            value -= width
    return value

def _create_random_genotype():
    """
    Create a random array genotype
    """
    genotype = np.array([], dtype=np.float64)
    for _ in range(LENGTH):
        #Append returns a copy
        genotype = np.append(genotype, random.uniform(RANGE_MIN, RANGE_MAX))
    return genotype
