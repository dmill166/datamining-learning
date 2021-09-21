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
os.chdir(os.path.abspath(''))
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

    print()