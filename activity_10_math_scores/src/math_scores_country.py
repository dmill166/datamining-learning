# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 10 - Box Plot Visualization

import os
import csv
import matplotlib.pyplot as plt 
import numpy as np
import sys

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname((__file__)))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME   = 'math_scores_country.csv'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, CSV_FILE_NAME)

if __name__ == "__main__":

    # TODO: Load csv data into Python
    if not os.path.isfile(CSV_FILE_PATH):
        print("Sorry, that doesn't exist!")
        sys.exit(1)
    print("Success! Found the file!")

    # TODO: extract scores from csv file, separating boys and girls data
    f_scores_list = []
    m_scores_list = []
    with open(CSV_FILE_PATH, 'rt') as csv_file:
        for line in csv_file:
            temp_dict = {}
            line_text = line.split(',')
            if line_text[2] == 'GIRL':
                temp_dict['country'] = [line_text[0]]
                temp_dict['score'] = [line_text[6]]
                f_scores_list.append(temp_dict)
            elif line_text[2] == 'BOY':
                temp_dict['country'] = [line_text[0]]
                temp_dict['score'] = [line_text[6]]
                m_scores_list.append(temp_dict)


    # TODO: produce a boxplot of boys and girls math scores, annotating median and whisker values


    # TODO: show the whisker values for boys and girls


    # TODO: list the countries that are outliers (below or above the whiskers)
