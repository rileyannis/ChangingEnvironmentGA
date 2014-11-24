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
import scipy.stats as stats
import fitness_function as ff
from math import floor

NUMBER_OF_ORGANISMS = None
MUTATION_RATE = None
NUMBER_OF_GENERATIONS = None
OUTPUT_FILE = None
ORG_TYPE = None
TOURNAMENT_SIZE = None
VERBOSE = False
ALTERNATE_ENVIRONMENT_CORR = None

def create_initial_population(fitness_function):
    population = []
    for _ in range(NUMBER_OF_ORGANISMS):
        if ORG_TYPE == "string":
            population.append(string_org.StringOrg(fitness_function))
        elif ORG_TYPE == "vector":
            population.append(real_value_vector_org.RealValueVectorOrg(fitness_function))
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
        #org_1 = random.choice(population)
        orgs = [random.choice(population) for i in range(TOURNAMENT_SIZE)]
        #new_population.append(get_better_organism(org_1, org_2))
        new_population.append(get_best_organism(orgs))
    return new_population

def get_best_organism(pop):
    best_fitness = -1
    if not pop[0].should_maximize_fitness:
        best_fitness = float("inf")
    best_org = None
    for org in pop:
        if (org.should_maximize_fitness and org.get_fitness() > best_fitness) \
                     or (not org.should_maximize_fitness and \
                     org.get_fitness() < best_fitness):
            best_org = org
            best_fitness = org.get_fitness()
    return best_org

def get_best_reference_organism(pop):
    best_fitness = -1
    if not pop[0].should_maximize_fitness:
        best_fitness = float("inf")
    best_org = None
    for org in pop:
        if (org.should_maximize_fitness and org.get_reference_fitness() > best_fitness) \
                     or (not org.should_maximize_fitness and \
                     org.get_reference_fitness() < best_fitness):
            best_org = org
            best_fitness = org.get_reference_fitness()
    return best_org

def get_better_organism(org1, org2):
    if (org1.should_maximize_fitness and (org1.get_fitness() > \
            org2.get_fitness())) or (not org1.should_maximize_fitness \
            and org1.get_fitness() < org2.get_fitness()):
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
    """Currently only works for vector orgs."""
    fitness_function = ff.Fitness_Function(ff.sphere_function, 0, real_value_vector_org.LENGTH)
    generations_average_fitness_list = [("Generation", "Average_Fitness", \
                    "Standard_Deviation", "Best_fitness", "Best_org")]
    population = create_initial_population(fitness_function)
    for gen in range(NUMBER_OF_GENERATIONS):
        if gen == int(floor(NUMBER_OF_GENERATIONS/3.0)):
            fitness_function.create_fitness2(ALTERNATE_ENVIRONMENT_CORR)
            fitness_function.set_flipped(True)
        elif gen == int(floor(NUMBER_OF_GENERATIONS*2.0/3.0)):
            fitness_function.set_flipped(False)
        population = get_next_generation(population)
        average_fitness = get_average_fitness(population)
        best_org = get_best_organism(population)
        best_fitness = best_org.get_fitness()
        stdev = stats.tstd([org.get_fitness() for org in population])

        reference_list = generations_average_fitness_list[:]
        #Create reference data set here

        generations_average_fitness_list.append((gen, average_fitness, \
                                    stdev, best_fitness, best_org))
        if VERBOSE:
            print_status(gen, population)
    return generations_average_fitness_list, fitness_function

def get_average_fitness(pop):
    total = 0
    for org in pop:
        total += org.get_fitness()
    return total / len(pop)

def get_average_reference_fitness(pop):
    total = 0
    for org in pop:
        total += org.get_reference_fitness()
    return total / len(pop)

def set_global_variables(args):
    global NUMBER_OF_ORGANISMS
    NUMBER_OF_ORGANISMS = args.number_of_organisms
    global MUTATION_RATE
    MUTATION_RATE = args.mutation_rate
    global NUMBER_OF_GENERATIONS
    NUMBER_OF_GENERATIONS = args.number_of_generations
    global TOURNAMENT_SIZE
    TOURNAMENT_SIZE = int(args.tournament_size)
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
        ff.MUTATION_EFFECT_SIZE = float(args.mutation_effect_size)
        real_value_vector_org.MUTATION_EFFECT_SIZE = float(args.mutation_effect_size)
    global OUTPUT_FILE
    OUTPUT_FILE = args.output_file
    global ALTERNATE_ENVIRONMENT_CORR
    ALTERNATE_ENVIRONMENT_CORR = float(args.alternate_environment_corr)
    global VERBOSE
    VERBOSE = args.verbose
    

def save_fitnesses_to_file(data):
    "Data is a list of tuples to be saved to a csv file"
    with open("fitnesses.csv", "wb") as f:
        writer = csv.writer(f)
        writer.writerows(data)

def save_corr_to_file(fitness_function):
    with open("correlation.txt", "w") as f:
        f.write(str(fitness_function.correlation()))

def generate_data():
    data, fitness_function = evolve_population()
    save_fitnesses_to_file(data)
    save_corr_to_file(fitness_function)

if __name__ == "__main__":
    s = string_org.StringOrg("xxxxxx")
    print(s)
    print(s.get_fitness())
    print(s.get_mutant())
