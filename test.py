#!/usr/bin/python
"""
Riley's first research project.
"""
import random

NUMBER_OF_ORGANISMS = 10
MAX_GENOTYPE = 100
MUTATION_RATE = 0.45
NUMBER_OF_GENERATIONS = 20

population = []
for _ in range(NUMBER_OF_ORGANISMS):
    org = random.randrange(1, MAX_GENOTYPE + 1)
    population.append(org)

for gen in range(NUMBER_OF_GENERATIONS):
    new_population = []
    for org in population:
        if random.random() < MUTATION_RATE:
            is_mutating_up = random.choice([True, False])
            if is_mutating_up:
                org += 1
            else:
                org -= 1
        org = min(org, 100)
        org = max(org, 0)
        new_population.append(org)

    new_new_population = []
    for _ in range(NUMBER_OF_ORGANISMS):
        org_1 = random.choice(new_population)
        org_2 = random.choice(new_population)
        new_new_population.append(max(org_1, org_2))

    population = new_new_population
    print("generation is: {}".format(gen))
    print("Population is: {}".format(population))
