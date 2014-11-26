import sys
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

output_dir_base = "junkdata"
config_files = ["test1_config.ini", "test2_config.ini"]
jobs = [convert_config_file_name_to_job(name, output_dir_base) for name in config_files]

for job in jobs:
    with open("tmp.sub", 'w') as f:
        f.write(common)
        f.write(job + '\n')
        print "----------Submitting----------"
    print common + job
    call(["qsub", 'tmp.sub'])
    call(["rm", 'tmp.sub']) 
