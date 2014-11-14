import random
from fitness_function import Fitness_Function, sphere_function

LENGTH = None

class RealValueVectorOrg(object):
    """
    this is a class that represents organisms as a real value vector
    fitness is determined by calling the fitness fuction
    the length is determined at object creation
    """

    should_maximize_fitness = False
    assert not LENGTH is None
    object_to_calculate_fitness = Fitness_Function(sphere_function, 0, LENGTH)

    def __init__(self, genotype=None):
        if genotype is None:
            genotype = create_random_genotype(LENGTH)
        assert LENGTH == len(genotype)
        self.genotype = genotype

    def get_fitness(self):
        return object_to_calculate_fitness.evaluate(self.genotype)

    def get_mutant(self):
        return RealValueVectorOrg(get_mutated_genotype(self.genotype))

    def __str__(self):
        return "RealValueVectorOrg({})".format(self.genotype)

    def __repr__(self):
        return str(self)

    def get_clone(self):
        return RealValueVectorOrg(self.genotype)

def get_mutated_genotype(genotype):
    "Mutates one locus in organism at random"
    mut_location = random.randrange(len(genotype))
    mut_value = random.uniform(-512, 512)
    mutant = genotype[:]
    mutant[mut_location] = mut_value
    return mutant

def create_random_genotype():
    genotype = []
    for _ in range(LENGTH):
        genotype.append(random.uniform(-512, 512))
    return genotype
