# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 09 - Visualization

import os
import sys
import csv
import matplotlib.pyplot as plt 
import numpy as np

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname((__file__)))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME   = 'weight_height.csv'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, CSV_FILE_NAME)

if __name__ == "__main__":

    # TODO: Load csv data into Python
    if not os.path.isfile(CSV_FILE_PATH):
        print("Sorry, that doesn't exist!")
        sys.exit(1)
    print("Success! Found the file!")

    # TODO: extract height and weight from csv file, separating female and male data
    f_height_list = []
    f_weight_list = []
    m_height_list = []
    m_weight_list = []
    with open(CSV_FILE_PATH, 'rt') as csv_file:
        for line in csv_file:
            line_text = line.split(',')
            if line_text[0] == '"Female"':
                f_height_list.append(float(line_text[1]))
                f_weight_list.append(float(line_text[2]))
            elif line_text[0] == '"Male"':
                m_height_list.append(float(line_text[1]))
                m_weight_list.append(float(line_text[2]))

    # TODO: produce a histograms of female weights with 10 bins starting at 53 and with 15 width
    counts, bins, _ = plt.hist(
    f_weight_list, 
    rwidth=.5,
    range=(55, 195),
    bins=[67.5, 82.5, 97.5, 112.5, 127.5, 142.5, 157.5, 172.5, 187.5]
    )
    plt.xlim([60, 200])
    plt.xticks(np.arange(60, 190, 15))
    plt.ylim([0, 1650])
    plt.yticks(np.arange(0, 1800, 200))
    plt.xlabel('Weight (pounds)')
    plt.ylabel('Female Count')
    plt.title('Female Weights')
    plt.show()

    # TODO: produce a scatter plot of male heights vs. weights 
    plt.scatter(m_height_list, m_weight_list)
    plt.grid()
    plt.xlabel('Height (inches)')
    plt.ylabel('Weights (pounds)')
    plt.title('Male Height x Weight')
    plt.show()

