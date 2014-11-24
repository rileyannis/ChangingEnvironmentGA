import sys
from subprocess import call
common = """
#!/bin/bash -login

#PBS -l walltime=00:00:30
#PBS -l nodes=1:ppn=1
#PBS -l mem=1gb
#PBS -N changing_environment_test
#PBS -t 1-10

module load NumPy
module load SciPy

cd ~/ChangingEnvironmentGA
"""

jobs = ["python changing_environment_ga.py -c test1_config.ini -o test_run1_${PBS_ARRAYID}",
        "python changing_environment_ga.py -c test2_config.ini -o test_run2_${PBS_ARRAYID}"]

for job in jobs:
    with open("tmp.sub", 'w') as f:
        f.write(common)
        f.write(job + '\n')
    # Remove this
    print "----------Submitting----------"
    print common + job
    call(["qsub", 'tmp.sub'])
    call(["rm", 'tmp.sub']) 
