import csv
import os
import pandas as pd
import cPickle
import random

def main():
    test_dir = "length_100_final"
    output_dir = "length_100_data"
    rounds = 1000
    #data = get_data(test_dir)
    data = get_pickled_data(test_dir)
    landscape_list = ["schafferf7", "sphere", "rana", "rosenbrock", "schwefel", "deceptive"]
#    multi_randomization_test(data, landscape_list, test_dir, rounds)
    for landscape in landscape_list:
        #modified_randomization_test(data, landscape, output_dir, rounds)
        average_correlation(data, landscape, output_dir, rounds)

def get_data(common_dir):
    """Version of get_data that doesn't use cPickle"""
    #Make a new dictionary
    data = {}
    #For each sub directory...
    for sub_dir in os.listdir(common_dir):
        #If it's not actually a directory, skip it
        if not os.path.isdir(common_dir + "/" + sub_dir):
            continue
        #Grab the meaningful config name
        sub_dir_name_list = sub_dir.split("/")[-1].split("_")
        config = "_".join(sub_dir_name_list[:-2])
        #Make sure the config name is in the dictionary
        if config not in data:
            data[config] = []
        #Get Correlation
        with open(common_dir+"/"+sub_dir+"/correlation.dat") as infile:
            corr = float(infile.readline())
        #Merge the rest of the data into one dataframe, merging on generation
        #Get Generation, Average_Fitness, and Standard_Deviation
        df = pd.read_csv(common_dir+"/"+sub_dir+"/experienced_fitnesses.csv")
        #Get Ref_Average_Fitness and Ref_Standard_Deviation
        df = df.merge(pd.read_csv(common_dir+"/"+sub_dir+"/reference_fitnesses.csv"), on="Generation")
        #Get Best_Fitness and Best_Org
        df = df.merge(pd.read_csv(common_dir+"/"+sub_dir+"/experienced_best_fitnesses.csv"), on="Generation")
        #Get Ref_Best_Fitness and Ref_Best_Org
        df = df.merge(pd.read_csv(common_dir+"/"+sub_dir+"/reference_best_fitnesses.csv"), on="Generation")
        #Append the correlation and dataframe to the associated list
        data[config].append([corr, df])
    return data

def get_pickled_data(common_dir):
    """Uses cPickle to store data the first time around so we can regenerate graphs later"""
    file_name = common_dir + "/pickled_data"
    try:
        data_file = open(file_name, "r")
        print("Using pickled data.")
        data = cPickle.load(data_file)
        data_file.close()
        return data
    except:
        print("Generating data.")
    data_file = open(file_name, "w")
    #Make a new dictionary
    data = {}
    #For each sub directory...
    for sub_dir in os.listdir(common_dir):
        #If it's not actually a directory, skip it
        if not os.path.isdir(common_dir + "/" + sub_dir):
            continue
        #Grab the meaningful config name
        sub_dir_name_list = sub_dir.split("/")[-1].split("_")
        config = "_".join(sub_dir_name_list[:-2])
        #Make sure the config name is in the dictionary
        if config not in data:
            data[config] = []
        #Get Correlation
        with open(common_dir+"/"+sub_dir+"/correlation.dat") as infile:
            corr = float(infile.readline())
        #Merge the rest of the data into one dataframe, merging on generation
        #Get Generation, Average_Fitness, and Standard_Deviation
        df = pd.read_csv(common_dir+"/"+sub_dir+"/experienced_fitnesses.csv")
        #Get Ref_Average_Fitness and Ref_Standard_Deviation
        df = df.merge(pd.read_csv(common_dir+"/"+sub_dir+"/reference_fitnesses.csv"), on="Generation")
        #Get Best_Fitness and Best_Org
        df = df.merge(pd.read_csv(common_dir+"/"+sub_dir+"/experienced_best_fitnesses.csv"), on="Generation")
        #Get Ref_Best_Fitness and Ref_Best_Org
        df = df.merge(pd.read_csv(common_dir+"/"+sub_dir+"/reference_best_fitnesses.csv"), on="Generation")
        #Append the correlation and dataframe to the associated list
        data[config].append([corr, df])
    cPickle.dump(data, data_file)
    data_file.close()
    return data

def randomization_test(data, key, directory, rounds):
    #Gather all of the average final fitnesses into a dictionary
    corr_dict = {}
    for config in data:
        if key == None or key in config:
            corr_dict[float(config.split("_")[1])] = []
            for run in range(len(data[config])):
                corr_dict[float(config.split("_")[1])].append(
                    float(data[config][run][1]["Ref_Average_Fitness"][-1:]))
    #Make a few variables
    output_data = [("Alternate Correlation", "Significance")]
    ctr_avg = sum(corr_dict[1.0])/len(corr_dict[1.0])
    #For each alternate correlation, get the difference between the control
    for alt_corr in corr_dict.keys():
        alt_avg = sum(corr_dict[alt_corr]) / len(corr_dict[alt_corr])
        diff = abs(alt_avg - ctr_avg)
        all_finals = corr_dict[1.0] + corr_dict[alt_corr]
        less_than = 0
        #Shuffle all the fitnesses, split them up, then get the difference rounds number of times
        for _ in range(rounds):
            random.shuffle(all_finals)
            lst1 = all_finals[:len(all_finals) / 2]
            lst2 = all_finals[len(all_finals) / 2:]
            rnd_diff = abs((sum(lst1) / len(lst1)) - (sum(lst2) / len(lst2)))
            #If the difference is less that the control difference, record it
            if rnd_diff < diff:
                less_than += 1
        #Output the alternate correlation and the percentage of differences less than the control
        output_data.append((alt_corr, 1.0 - (float(less_than) / float(rounds))))
    #Save output to file
    filename = directory + "/randomiztion_test_" + key + "_" + str(rounds) + "_rounds.csv"
    with open(filename, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(output_data)

def average_correlation(data, key, directory, rounds):
    corr_dict = {}
    for config in data:
        if key == None or key in config:
            corr_dict[float(config.split("_")[1])] = []
            for run in range(len(data[config])):
                corr_dict[float(config.split("_")[1])].append(
                    float(data[config][run][0]))
    output_data = [("Alternate Correlation", "Actual Correlation")]
    for alt_corr in corr_dict.keys():
        output_data.append((alt_corr, (sum(corr_dict[alt_corr]) / float(len(corr_dict[alt_corr])))))
    filename = directory + "/average_correlation_" + key + ".csv"
    with open(filename, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(output_data)

def modified_randomization_test(data, key, directory, rounds):
    #Gather all of the average final fitnesses into a dictionary
    corr_dict = {}
    for config in data:
        if key == None or key in config:
            corr_dict[float(config.split("_")[1])] = []
            for run in range(len(data[config])):
                corr_dict[float(config.split("_")[1])].append(
                    float(data[config][run][1]["Ref_Average_Fitness"][-1:]))
    #Make a few variables
    output_data = [("Alternate Correlation", "Significance")]
    ctr_avg = sum(corr_dict[1.0])/len(corr_dict[1.0])
    #For each alternate correlation, get the difference between the control
    for alt_corr in corr_dict.keys():
        alt_avg = sum(corr_dict[alt_corr]) / len(corr_dict[alt_corr])
        #Not absolute value
        diff = ctr_avg - alt_avg
        all_finals = corr_dict[1.0] + corr_dict[alt_corr]
        less_than = 0
        #Shuffle all the fitnesses, split them up, then get the difference rounds number of times
        for _ in range(rounds):
            random.shuffle(all_finals)
            lst1 = all_finals[:len(all_finals) / 2]
            lst2 = all_finals[len(all_finals) / 2:]
            #Not absolute value
            rnd_diff = (sum(lst1) / len(lst1)) - (sum(lst2) / len(lst2))
            #If the difference is less that the control difference, record it
            if rnd_diff < diff:
                less_than += 1
        #Output the alternate correlation and the percentage of differences less than the control
        output_data.append((alt_corr, (float(less_than) / float(rounds))))
    #Save output to file
    filename = directory + "/modified_randomiztion_test_" + key + "_" + str(rounds) + "_rounds.csv"
    with open(filename, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(output_data)

def multi_randomization_test(data, lst, directory, rounds):
    output_data = [["Alternate Correlation"]]
    output_dict = {}
    for key in lst:
#Gather all of the average final fitnesses into a dictionary
        corr_dict = {}
        for config in data:
            if key == None or key in config:
                corr_dict[float(config.split("_")[1])] = []
                if float(config.split("_")[1]) not in output_dict.keys():
                    output_dict[float(config.split("_")[1])] = []
                for run in range(len(data[config])):
                    corr_dict[float(config.split("_")[1])].append(
                        float(data[config][run][1]["Ref_Average_Fitness"][-1:]))
#Make a few variables
        output_data[0].append(key)
        ctr_avg = sum(corr_dict[1.0])/len(corr_dict[1.0])
#For each alternate correlation, get the difference between the control
        for alt_corr in corr_dict.keys():
            alt_avg = sum(corr_dict[alt_corr]) / len(corr_dict[alt_corr])
        #Not absolute value
            diff = ctr_avg - alt_avg
            all_finals = corr_dict[1.0] + corr_dict[alt_corr]
            less_than = 0
        #Shuffle all the fitnesses, split them up, then get the difference rounds number of times
            for _ in range(rounds):
                random.shuffle(all_finals)
                lst1 = all_finals[:len(all_finals) / 2]
                lst2 = all_finals[len(all_finals) / 2:]
            #Not absolute value
                rnd_diff = (sum(lst1) / len(lst1)) - (sum(lst2) / len(lst2))
            #If the difference is less that the control difference, record it
                if rnd_diff < diff:
                    less_than += 1
        #Output the alternate correlation and the percentage of differences less than the control
            output_dict[alt_corr].append(float(less_than) / float(rounds))
    #Save output to file
    for key in sorted(output_dict.keys(), reverse=True):
        output_data.append([key].extend(output_dict[key]))
    filename = directory + "/multi_randomiztion_test_" + str(rounds) + "_rounds.csv"
    with open(filename, "wb") as f:
        writer = csv.writer(f)
        writer.writerows(output_data)

if __name__ == "__main__":
    main()
        
