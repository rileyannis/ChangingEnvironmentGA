#!/usr/bin/python
"""
Riley's first research project.
"""
from __future__ import division
import random
from string import ascii_uppercase
import csv
import string_org
import real_value_vector_org
from data_handling import init_file, log_fitness

NUMBER_OF_ORGANISMS = None
MUTATION_RATE = None
NUMBER_OF_GENERATIONS = None
OUTPUT_FILE = None
ORG_TYPE = None

def create_initial_population():
    population = []
    for _ in range(NUMBER_OF_ORGANISMS):
        if ORG_TYPE == "string":
            population.append(string_org.StringOrg())
        elif ORG_TYPE == "vector":
            population.append(real_value_vector_org.RealValueVectorOrg())
    return population


def get_mutated_population(population):
    new_population = []
    for org in population:
        if random.random() < MUTATION_RATE:
            new_org = org.get_mutant()
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
    """
    fix me!!!!!!
    """
    best_org = get_best_organism(pop)
    new_population = [best_org]
    while len(new_population) < NUMBER_OF_ORGANISMS:
        new_population.append(best_org.get_mutant())
    return new_population

def get_best_organism(pop):
    best_fitness = -1
    best_org = None
    for org in pop:
        if org.get_fitness() > best_fitness:
            best_org = org
            best_fitness = org.get_fitness()
    return best_org

def get_better_organism(org1, org2):
    if org1.should_maximize_fitness and (org1.get_fitness() > org2.get_fitness()):
        return org1
    return org2

def get_next_generation(population):
    new_population = get_mutated_population(population)
    new_new_population = get_selected_population_soft(new_population)
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
        print_status(gen, population)
        log_fitness(population)
    return generations_average_fitness_list

def get_average_fitness(pop):
    total = 0
    for org in pop:
        total += org.get_fitness()
    return total / len(pop)

def set_global_variables(args):
    global NUMBER_OF_ORGANISMS
    NUMBER_OF_ORGANISMS = args.number_of_organisms
    global MUTATION_RATE
    MUTATION_RATE = args.mutation_rate
    global NUMBER_OF_GENERATIONS
    NUMBER_OF_GENERATIONS = args.number_of_generations
    global ORG_TYPE
    ORG_TYPE = args.org_type
    if args.org_type == "string":
        string_org.TARGET_STRING = args.target_string
        string_org.LETTERS = args.letters
    elif args.org_type == "vector":
        real_value_vector_org.LENGTH = int(args.length)
        range_list = args.range.strip("()").split(",")
        range_list = [int(x.strip()) for x in range_list]
        real_value_vector_org.RANGE = tuple(range_list)
    global OUTPUT_FILE
    OUTPUT_FILE = args.output_file

def save_to_file(data):
    "Data is a list of tuples to be saved to a csv file"
    with open(OUTPUT_FILE, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(data)

def generate_data():
    init_file()
    data = evolve_population()
    save_to_file(data)

if __name__ == "__main__":
    s = string_org.StringOrg("xxxxxx")
    print(s)
    print(s.get_fitness())
    print(s.get_mutant())
