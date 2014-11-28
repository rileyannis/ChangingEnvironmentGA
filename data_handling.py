import csv
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def main():
    test_dir = "experiment_1"
    data = get_data(test_dir)
    plot_average_final_fitness(data, test_dir)

def get_data(common_dir):
    data = {}
    for d in os.listdir(common_dir):
        dir_name_list = d.split("/")[-1].split("_")
        idnum = dir_name_list[-1]
        config = "_".join(dir_name_list[:-1])
        if config in data:
            data[config][idnum] = {}
        else:
            data[config] = {}
            data[config][idnum] = {}

        with open(common_dir+"/"+d+"/correlation.dat") as infile:
            data[config][idnum]["correlation"] = float(infile.readline())

        data[config][idnum]["average_experienced"] = \
                pd.read_csv(common_dir+"/"+d+"/experienced_fitnesses.csv")
        data[config][idnum]["average_reference"] = \
                pd.read_csv(common_dir+"/"+d+"/reference_fitnesses.csv")
        data[config][idnum]["best_experienced"] = \
                pd.read_csv(common_dir+"/"+d+"/experienced_best_fitnesses.csv")
        data[config][idnum]["best_reference"] = \
                pd.read_csv(common_dir+"/"+d+"/reference_best_fitnesses.csv")

    return data

def plot_average_final_fitness(data, directory="."):
    corrs = []
    finals = []
    
    for config in data:
        for run in data[config]:
            corrs.append(data[config][run]["correlation"])
            finals.append(float(data[config][run]["average_reference"]["Average_Fitness"][-1:]))

    plt.plot(corrs, finals, ".")
    plt.savefig(directory+"/correlation_vs_final_fitness_scatter.png")

if __name__ == "__main__":
    main()
        
