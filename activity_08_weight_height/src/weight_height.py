# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 08 - Summarization

import os
import csv
import numpy as np
import sys
from numpy.lib.function_base import corrcoef

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname((__file__)))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME = 'weight_height.csv'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, CSV_FILE_NAME)

if __name__ == "__main__":

    if not os.path.isfile(CSV_FILE_PATH):
        print("Sorry, that doesn't exist!")
        sys.exit(1)
    print("Success! Found the file!")

    # TODO: extract height and weight from csv file, separating female and male data
    f_height_list = []
    f_weight_list = []
    m_height_list = []
    m_weight_list = []
    with open(os.path.join(DATA_FOLDER, CSV_FILE_NAME), 'rt') as csv_file:
        for line in csv_file:
            line_text = line.split(',')
            if line_text[0] == '"Female"':
                f_height_list.append(float(line_text[1]))
                f_weight_list.append(float(line_text[2]))
            elif line_text[0] == '"Male"':
                m_height_list.append(float(line_text[1]))
                m_weight_list.append(float(line_text[2]))

    # TODO: compute and display stats summary info for female and male: heigh (range, mean and std), weight (range, mean and std), and correlation coefficient between height and weight
    lists = [f_height_list, f_weight_list, m_height_list, m_weight_list]
    desc_lists = ['Female heights: ', 'Female weights: ', 'Male heights: ', 'Male weights: ']
    np_arrays = []
    a = 0
    for a in range(0, len(lists)):
        np_arrays.append(np.array(lists[a]))

    b = 0
    for b in range(0, len(np_arrays)):
        print('\n', desc_lists[b], sep='')
        print('range: ', round(np.min(np_arrays[b]), 2), '..', round(np.max(np_arrays[b]), 2), sep='')
        print('mean:', round(np.average(np_arrays[b]), 2))
        print('std:', round(np.std(np_arrays[b]), 2), '\n')
        if b % 2 == 1:
            print('Corr coeff:', round(np.corrcoef(np_arrays[b - 1], np_arrays[b])[0, 1], 4), '\n')

    # f_height_data = np.array(f_height_list)
    # print('\n\nFemale height:')
    # print('range: ', np.min(f_height_data), '..', np.max(f_height_data), sep='')
    # print('mean:', np.average(f_height_data))
    # print('std:', np.std(f_height_data), '\n')

    # m_height_data = np.array(m_height_list)
    # print('Male height:')
    # print('range: ', np.min(m_height_data), '..', np.max(m_height_data), sep='')
    # print('mean:', np.average(m_height_data))
    # print('std:', np.std(m_height_data), '\n')

    # f_weight_data = np.array(f_weight_list)
    # print('Female height:')
    # print('range: ', np.min(f_weight_data), '..', np.max(f_weight_data), sep='')
    # print('mean:', np.average(f_weight_data))
    # print('std:', np.std(f_weight_data), '\n')

    # m_weight_data = np.array(m_weight_list)
    # print('Female height:')
    # print('range: ', np.min(m_weight_data), '..', np.max(m_weight_data), sep='')
    # print('mean:', np.average(m_weight_data))
    # print('std:', np.std(m_weight_data), '\n')


def midterm():
    import numpy as np
    import matplotlib.pyplot as plt

    ppl_grades = [8.5, 9.1, 9.5, 8, 7.9, 2.3, 8.8, 9, 10, 1, 9.5, 8.2, 8, 9.8, 8, 7.5, 10, 9.9, 7.8, 9.2]

    # TODO: summary statistics
    print('*** Summary Statistics ***')

    # TODO: boxplot
    plt.show()


midterm()
