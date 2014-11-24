import random
from fitness_function import Fitness_Function, sphere_function, MUTATION_EFFECT_SIZE

LENGTH = None
RANGE = None

class RealValueVectorOrg(object):
    """
    this is a class that represents organisms as a real value vector
    fitness is determined by calling the fitness fuction
    the length is determined at object creation
    """

    def __init__(self, fitness_function, genotype=None):
        self.should_maximize_fitness = False
        self.object_to_calculate_fitness = fitness_function

        if genotype is None:
            genotype = create_random_genotype()
        assert LENGTH == len(genotype)
        self.genotype = genotype
        self.fitness_function = fitness_function

    def get_fitness(self):
        return self.object_to_calculate_fitness.evaluate(self.genotype)

    def get_reference_fitness(self):
        return self.object_to_calculate_fitness.fitness1_fitness(self.genotype)

    def get_alternate_fitness(self):
        return self.object_to_calculate_fitness.fitness2_fitness(self.genotype)

    def get_mutant(self):
        return RealValueVectorOrg(self.fitness_function, \
                                  get_mutated_genotype(self.genotype))

    def __str__(self):
        return "RealValueVectorOrg({})".format(self.genotype)

    def __repr__(self):
        return str(self)

    def get_clone(self):
        return RealValueVectorOrg(self.fitness_function, self.genotype)

def get_mutated_genotype(genotype):
    "Mutates one locus in organism at random"
    mut_location = random.randrange(len(genotype))
    mut_value = random.normalvariate(0, MUTATION_EFFECT_SIZE)
    mutant = genotype[:]
    mutant[mut_location] += mut_value

    #wraparound if range exceeded
    if mutant[mut_location] < RANGE[0]: 
        mutant[mut_location] = RANGE[1] + RANGE[0] - mutant[mut_location]
    elif mutant[mut_location] > RANGE[1]:
        mutant[mut_location] = RANGE[0] + mutant[mut_location] - RANGE[1]

    return mutant

def create_random_genotype():
    genotype = []
    for _ in range(LENGTH):
        genotype.append(random.uniform(RANGE[0], RANGE[1]))
    return genotype
