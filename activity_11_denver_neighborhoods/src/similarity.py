# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 11: similarity analysis of neighborhoods in the Denver metro area

import csv 
import re 
import os
import math
import matplotlib.pyplot as plt 
from matplotlib import cm as cm

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname((__file__)))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME = 'denver_neighborhoods.csv'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, CSV_FILE_NAME)

def min_max(data, mins, maxs, interval=(0,1)):
    return [ int(((data[i] - mins[i]) / (maxs[i] - mins[i]) * (interval[1] - interval[0]) + interval[0]) * 100000) / 100000 for i in range(len(data))]

def eucl_dist(a, b): 
    sum = 0
    for i in range(len(a)):
        sum += (a[i] - b[i])**2
    return int((1 - math.sqrt(sum / len(a))) * 100000) / 100000

# TODO: finish the similarity analysis
if __name__ == "__main__":

    neighborhoods = []
    matrix = []
    with open(os.path.join(DATA_FOLDER, CSV_FILE_NAME), 'rt') as csv_file:
        reader = csv.reader(csv_file)
        row_count = 0
        for row in reader:
            row_count += 1
            if row_count == 1:
                continue
            row[0] = re.sub('Washington', 'Was.', row[0])
            row[0] = re.sub('South', 'S.', row[0])
            neighborhoods.append(row[0])
            data = [ int(row[1]), int(row[2]), float(row[3]), int(row[4]), float(row[5])]
            if row_count == 2:
                mins = list(data)
                maxs = list(data)
            else:
                for i in range(len(data)):
                    mins[i] = min(mins[i], data[i])
                    maxs[i] = max(maxs[i], data[i])
            matrix.append(data)
    # print(mins)
    # print(maxs)
    matrix = [ min_max(data, mins, maxs) for data in matrix ]
    # print(matrix)
    

    print(matrix[0])
    print(matrix[1])
    print(eucl_dist(matrix[0], matrix[0]))
    print(eucl_dist(matrix[1], matrix[0]))
    print(eucl_dist(matrix[2], matrix[0]))
    
    dm = []
    for i in range(len(matrix)):
        row = []
        for j in range(len(matrix)):
            row.append(eucl_dist(matrix[i], matrix[j]))
        dm.append(row)
    plt.rc('font', size=8) 
    cmap = cm.get_cmap('YlOrBr')
    img = plt.matshow(dm, cmap=cmap)
    axes = plt.gca()
    axes.set_yticks(list(range(len(neighborhoods))))
    axes.set_yticklabels(neighborhoods)
    axes.set_xticks(list(range(len(neighborhoods))))
    axes.set_xticklabels(neighborhoods, rotation=90)
    fig = plt.gcf() # reference to the plot
    ticks = [x / 10 for x in range(1, 11)]
    fig.colorbar(img, ticks=ticks)
    # fig.subplots_adjust(top=0.2)
    plt.show()

