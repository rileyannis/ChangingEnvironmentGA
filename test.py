#!/usr/bin/python
"""
Riley's first research project.
"""
import random

NUMBER_OF_ORGANISMS = 10
MAX_GENOTYPE = 100
MUTATION_RATE = 0.45
NUMBER_OF_GENERATIONS = 20




def create_initial_population():
    population = []
    for _ in range(NUMBER_OF_ORGANISMS):
        org = random.randrange(1, MAX_GENOTYPE + 1)
        population.append(org)
    return population

def get_mutated_organism(org):
    is_mutating_up = random.choice([True, False])
    if is_mutating_up:
        new_org = org + 1
    else:
        new_org = org - 1
    new_org = min(new_org, 100)
    new_org = max(new_org, 0)
    return new_org




population = create_initial_population()

for gen in range(NUMBER_OF_GENERATIONS):
    new_population = []
    for org in population:
        if random.random() < MUTATION_RATE:
            new_org = get_mutated_organism(org)
            new_population.append(new_org)
        else:
            new_population.append(org)

    new_new_population = []
    for _ in range(NUMBER_OF_ORGANISMS):
        org_1 = random.choice(new_population)
        org_2 = random.choice(new_population)
        new_new_population.append(max(org_1, org_2))
    population = new_new_population
    print("generation is: {}".format(gen))
    print("Population is: {}".format(population))
