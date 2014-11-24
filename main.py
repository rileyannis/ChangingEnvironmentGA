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
import os
import shutil

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
        orgs = [random.choice(population) for _ in range(TOURNAMENT_SIZE)]
        new_population.append(get_best_organism(orgs))
    return new_population

def get_best_organism(pop, reference=False):
    best_fitness = -1
    if not pop[0].should_maximize_fitness:
        best_fitness = float("inf")
    best_org = None
    for org in pop:
        fitness = org.get_reference_fitness() if reference else org.get_fitness()
        if (org.should_maximize_fitness and fitness > best_fitness) \
                     or (not org.should_maximize_fitness and \
                     fitness < best_fitness):
            best_org = org
            best_fitness = fitness
    return best_org

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
        average_reference_fitness = get_average_reference_fitness(population)
        best_reference_org = get_best_organism(population, reference=True)
        best_reference_fitness = best_reference_org.get_reference_fitness()
        stdev_reference = stats.tstd([org.get_reference_fitness() for org in population])
        reference_list.append((gen, average_reference_fitness, \
                                    stdev_reference, best_reference_fitness, best_reference_org))

        generations_average_fitness_list.append((gen, average_fitness, \
                                    stdev, best_fitness, best_org))
        if VERBOSE:
            print_status(gen, population)
    return generations_average_fitness_list, reference_list,  fitness_function

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

def set_global_variables(config):
    global OUTPUT_FOLDER
    OUTPUT_FOLDER = config.get("DEFAULT", "output_folder")
    global CONFIG_FILE
    CONFIG_FILE = config.get("DEFAULT", "config_file")
    global VERBOSE
    VERBOSE = config.getboolean("DEFAULT", "verbose")
    global NUMBER_OF_ORGANISMS
    NUMBER_OF_ORGANISMS = config.getint("DEFAULT", "number_of_organisms")
    global MUTATION_RATE
    MUTATION_RATE = config.getfloat("DEFAULT", "mutation_rate")
    global NUMBER_OF_GENERATIONS
    NUMBER_OF_GENERATIONS = config.getint("DEFAULT", "number_of_generations")
    global TOURNAMENT_SIZE
    TOURNAMENT_SIZE = config.getint("DEFAULT", "tournament_size")
    global ORG_TYPE
    ORG_TYPE = config.get("DEFAULT", "org_type")
    if ORG_TYPE == "string":
        string_org.TARGET_STRING = config.get("DEFAULT", "target_string")
        string_org.LETTERS = config.get("DEFAULT", "letters")
    elif ORG_TYPE == "vector":
        real_value_vector_org.LENGTH = config.getint("DEFAULT", "length")
        range_minimum = config.getint("DEFAULT", "range_minimum")
        real_value_vector_org.RANGE_MIN = range_minimum
        range_maximum = config.getint("DEFAULT", "range_maximum")
        real_value_vector_org.RANGE_MAX = range_maximum
        mut_effect_size = config.getfloat("DEFAULT", "mutation_effect_size")
        ff.MUTATION_EFFECT_SIZE = mut_effect_size
        real_value_vector_org.MUTATION_EFFECT_SIZE = mut_effect_size
    global ALTERNATE_ENVIRONMENT_CORR
    ALTERNATE_ENVIRONMENT_CORR = config.getfloat(
        "DEFAULT", "alternate_environment_corr")
    
def save_fitnesses_to_file(fitnesses, filename):
    with open(filename, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(fitnesses)

def save_corr_to_file(fitness_function, filename):
    with open(filename, "w") as f:
        f.write(str(fitness_function.correlation()))

def generate_data():
    experienced_fits, reference_fits, fitness_function = evolve_population()
    if os.path.exists(OUTPUT_FOLDER):
        raise IOError("output_folder: {} already exists".format(OUTPUT_FOLDER))
    os.mkdir(OUTPUT_FOLDER)
    config_filename = os.path.basename(CONFIG_FILE)
    config_dest = os.path.join(OUTPUT_FOLDER, config_filename)
    shutil.copyfile(CONFIG_FILE, config_dest)
    
    experienced_filename = os.path.join(
        OUTPUT_FOLDER, "experienced_fitnesses.csv")
    reference_filename = os.path.join(
        OUTPUT_FOLDER, "reference_fitnesses.csv")
    corr_filename = os.path.join(
        OUTPUT_FOLDER, "correlation.dat")

    save_fitnesses_to_file(experienced_fits, experienced_filename)
    save_fitnesses_to_file(reference_fits, reference_filename)
    save_corr_to_file(fitness_function, corr_filename)

