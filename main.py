#!/usr/bin/python
"""
Riley's first research project.
"""
from __future__ import division
import random
from string import ascii_uppercase
import csv

NUMBER_OF_ORGANISMS = None
MUTATION_RATE = None
NUMBER_OF_GENERATIONS = None
TARGET_STRING = None
LETTERS = None
OUTPUT_FILE = None

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
    "Mutates one character in organism at random"
    mut_location = random.randrange(len(TARGET_STRING))
    while True:
        mut_letter = random.choice(LETTERS)
        if mut_letter != org[mut_location]:
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
    "Returns the number of matching letters between org and target"
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
    generations_average_fitness_list = [("Generation","Average_Fitness")]
    population = create_initial_population()
    for gen in range(NUMBER_OF_GENERATIONS):
        population = get_next_generation(population)
        average_fitness = get_average_fitness(population)
        generations_average_fitness_list.append((gen, average_fitness))
    return generations_average_fitness_list

def get_average_fitness(pop):
    total = 0
    for org in pop:
        total += get_fitness(org)
    return total / len(pop)

def set_global_variables(args):
    global NUMBER_OF_ORGANISMS
    NUMBER_OF_ORGANISMS = args.number_of_organisms
    global MUTATION_RATE
    MUTATION_RATE = args.mutation_rate
    global NUMBER_OF_GENERATIONS
    NUMBER_OF_GENERATIONS = args.number_of_generations
    global TARGET_STRING
    TARGET_STRING = args.target_string
    global LETTERS
    LETTERS = args.letters
    global OUTPUT_FILE
    OUTPUT_FILE = args.output_file

def save_to_file(data):
    "Data is a list of tuples to be saved to a csv file"
    with open(OUTPUT_FILE, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(data)

def generate_data():
    data = evolve_population()
    save_to_file(data)
