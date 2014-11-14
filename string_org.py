import random

TARGET_STRING = "aaabbc"
LETTERS = "abcd"

class StringOrg(object):
    """
    this is a class that represents organisms as a string
    fitness equals distance to the target string
    """

    should_maximize_fitness = True

    def __init__(self, genotype=None):
        if genotype is None:
            genotype = create_random_genotype()
        assert len(genotype) == len(TARGET_STRING)
        self.genotype = genotype

    def get_fitness(self):
        return get_fitness(self.genotype)

    def get_mutant(self):
        return StringOrg(get_mutated_genotype(self.genotype))

    def __str__(self):
        return "StringOrg(\"{}\")".format(self.genotype)

    def __repr__(self):
        return str(self)

    def get_clone(self):
        return StringOrg(self.genotype)

def get_mutated_genotype(genotype):
    "Mutates one character in organism at random"
    mut_location = random.randrange(len(TARGET_STRING))
    while True:
        mut_letter = random.choice(LETTERS)
        if mut_letter != genotype[mut_location]:
            return genotype[:mut_location] + mut_letter + genotype[mut_location + 1:]

def get_fitness(org):
    "Returns the number of matching letters between org and target"
    matches = 0
    for i in range(len(TARGET_STRING)):
        if TARGET_STRING[i] == org[i]:
            matches += 1
    return matches

def create_random_genotype():
    genotype = []
    for _ in range(len(TARGET_STRING)):
        genotype.append(random.choice(LETTERS))
    return "".join(genotype)
