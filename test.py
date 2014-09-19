#!/usr/bin/python
"""
Riley's first research project.
"""
from __future__ import division
import random
from string import ascii_uppercase

NUMBER_OF_ORGANISMS = 200
MUTATION_RATE = 0.90
NUMBER_OF_GENERATIONS = 1000
TARGET_STRING = "METHINKS IT IS LIKE A WEASEL"
LETTERS = ascii_uppercase + " "

def create_initial_population():
    population = []
    for _ in range(NUMBER_OF_ORGANISMS):
        population.append(create_random_organism())
    return population

def create_random_organism():
    genotype = []
    for _ in range(len(TARGET_STRING)):
        genotype.append(random.choice(LETTERS))
    return "".join(genotype)

def get_mutated_organism(org):
    mut_location = random.randrange(len(TARGET_STRING))
    mut_letter = random.choice(LETTERS)
    return org[:mut_location] + mut_letter + org[mut_location + 1:]

def get_mutated_population(population):
    new_population = []
    for org in population:
        if random.random() < MUTATION_RATE:
            new_org = get_mutated_organism(org)
            new_population.append(new_org)
        else:
            new_population.append(org)
    return new_population

def get_selected_population_soft(population):
    new_population = []
    for _ in range(NUMBER_OF_ORGANISMS):
        org_1 = random.choice(population)
        org_2 = random.choice(population)
        new_population.append(get_better_organism(org_1, org_2))
    return new_population

def get_selected_population(pop):
    best_org = get_best_organism(pop)
    new_population = [best_org]
    while len(new_population) < NUMBER_OF_ORGANISMS:
        new_population.append(get_mutated_organism(best_org))
    return new_population

def get_best_organism(pop):
    best_fitness = -1
    best_org = None
    for org in pop:
        if get_fitness(org) > best_fitness:
            best_org = org
            best_fitness = get_fitness(org)
    return best_org

def get_better_organism(org1, org2):
    if get_fitness(org1) > get_fitness(org2):
        return org1
    return org2

def get_fitness(org):
    matches = 0
    for i in range(len(TARGET_STRING)):
        if TARGET_STRING[i] == org[i]:
            matches += 1
    return matches

def get_next_generation(population):
    new_population = get_mutated_population(population)
    new_new_population = get_selected_population(new_population)
    return new_new_population

def print_status(generation, population):
    average_fitness = get_average_fitness(population)
    print("Gen = {}  Pop = {}  Fit = {}".format(generation, population, average_fitness))

def evolve_population():
    population = create_initial_population()
    for gen in range(NUMBER_OF_GENERATIONS):
        population = get_next_generation(population)
        print_status(gen, population)

def get_average_fitness(pop):
    total = 0
    for org in pop:
        total += get_fitness(org)
    return total / len(pop)

if __name__ == "__main__":
    evolve_population()
