import sys
import itertools
from subprocess import call

array_size = 10

def convert_config_file_name_to_job(file_name, output_dir_base):
    return "python changing_environment_ga.py -c {0} -o {1}/{0}_${{PBS_ARRAYID}}".format(file_name, output_dir_base)

common = """
#!/bin/bash -login

#PBS -l walltime=00:00:30
#PBS -l nodes=1:ppn=1
#PBS -l mem=1gb
#PBS -N changing_environment_test
#PBS -t 1-{0}

module load NumPy
module load SciPy

cd ~/ChangingEnvironmentGA
""".format(array_size)


config_common = """
[DEFAULT]
fitness_function_type = {0}
number_of_organisms = 500
mutation_rate = 0.20
number_of_generations = 2000
org_type = vector
length = 20
range_minimum = -512
range_maximum = 512
tournament_size = 2
mutation_effect_size = 10
alternate_environment_corr = {1}
verbose = False
"""
alt_corrs = [-1, -0.5, 0, 0.5, 1]
function_types = ["sphere", "rosenbrock"]

def write_to_file(filename, contents):
    with open(filename, "w") as file_handle:
        file_handle.write(contents)


if __name__ == "__main__":
    config_files = []

    for function_type, alt_corr in itertools.product(function_types, alt_corrs):
        config_filename = "{}_{}.ini".format(function_type, alt_corr)
        contents = config_common.format(function_type, alt_corr)
        write_to_file(config_filename, contents)
        config_files.append(config_filename)

    output_dir_base = "junkdata1"
    jobs = [convert_config_file_name_to_job(name, output_dir_base) for name in config_files]


    for job in jobs:
        contents = common + "\n" + job + "\n"
        write_to_file("tmp.sub", contents)
        print "----------Submitting----------"
        print contents
        call(["qsub", 'tmp.sub'])
        call(["rm", 'tmp.sub']) 
