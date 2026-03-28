# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Homework 03 - HDI Visualization

# Resources:
# Used the following when determining data structure I wanted to use:
#   https://stackoverflow.com/questions/44833822/specify-length-of-sequence-or-list-with-python-typing-module
#
# Researched handling intra-line commas; was directed to the csv library:
#   https://stackoverflow.com/questions/7682561/how-do-i-split-a-line-by-commas-but-ignore-commas-within-quotes-python
#
# Attempted to locate useful resources for Python matplotlib histograms; no useful sources found
# 
# Used this video to illustrate setting title and axis parameters:
#   https://www.youtube.com/watch?v=XDv6T4a0RNc
#
# Used this sample to influence my tick marks and axes formatting
#   https://stackoverflow.com/questions/58585241/modify-the-x-axis-labels-in-histogram-plot-using-matplotlib

import os
import csv
import matplotlib.pyplot as plt
import sys
import numpy as np

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname((__file__)))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
HDI_FILE_NAME = 'hdi.csv'
HDI_FILE_PATH = os.path.join(DATA_FOLDER, HDI_FILE_NAME)
TARGET_YEAR = '2019'

if __name__ == "__main__":

    # TODO: validate CSV exists
    if not os.path.isfile(HDI_FILE_PATH):
        print("Sorry, that doesn't exist!")
        sys.exit(1)
    print("Success! Found the file!")

    # TODO: extract column data from csv file into a list of dictionaries
    list_of_dicts = []
    first_row = True
    column_headers = []

    with open(HDI_FILE_PATH, 'rt') as f:
        reader = csv.reader(f)
        for row in reader:
            if first_row:
                for a in range(0, len(row)):
                    column_headers.append(row[a].strip())
                first_row = False
            else:
                row_dict = {}
                for i in range(0, len(row)):
                    row_dict[column_headers[i]] = row[i].strip()
                list_of_dicts.append(row_dict)

    # TODO: Extract country name and HDI for TARGET_YEAR
    hdi_data_one_year = {}
    for j in range(0, len(list_of_dicts)):
        temp_dict = list_of_dicts[j]
        if temp_dict.get('Coverage') == 'Country':
            country_name = temp_dict.get('Country')
            hdi_one_year_float = float(temp_dict.get(TARGET_YEAR))
            hdi_data_one_year[country_name] = [hdi_one_year_float]

    # TODO: Create histogram for country name and target year
    plot_values = []
    for x in hdi_data_one_year.values():
        plot_values.append(x[0])
    counts, bins, _ = plt.hist(
        plot_values,
        range=(.25, 1.05),
        bins=[.3, .4, .5, .6, .7, .8, .9, 1.0],
        rwidth=0.9
    )
    plt.xlim([.25, 1.05])
    plt.xticks(np.arange(.35, 1.05, .1))
    plt.ylim([0, 60])
    plt.yticks(np.arange(0, 60, 10))
    plt.xlabel('HDI')
    plt.ylabel('Number of Countries')
    plt.title('Human Development Index (HDI) in the World (' + TARGET_YEAR + ')')
    plt.show()
