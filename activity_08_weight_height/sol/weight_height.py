# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 08 - Summarization

import os
import csv
import numpy as np
from numpy.lib.function_base import corrcoef

# definitions/parameters
DATA_FOLDER = os.path.join('..', 'data')
FILE_NAME   = 'weight_height.csv'

if __name__ == "__main__":

    # TODO: extract height and weight from csv file, separating female and male data
    height_females = []
    height_males   = []
    weight_females = []
    weight_males   = []

    with open(os.path.join(DATA_FOLDER, FILE_NAME), 'rt') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader: 
            if row['Gender'] == 'Female':
                height_females.append(float(row['Height']))
                weight_females.append(float(row['Weight']))
            else:
                height_males.append(float(row['Height']))
                weight_males.append(float(row['Weight']))

    # TODO: compute and display stats summary info for female and male: heigh (range, mean and std), weight (range, mean and std), and correlation coefficient between height and weight
    height_females = np.array(height_females)
    height_males   = np.array(height_males)
    weight_females = np.array(weight_females)
    weight_males   = np.array(weight_males)

    print('*** Females Summary ***')
    print('Height range: [{:.2f}..{:.2f}]'.format(np.min(height_females), np.max(height_females)))
    print('Height mean: {:.2f}'.format(np.mean(height_females)))
    print('Height std: {:.2f}'.format(np.std(height_females)))
    print('Weight range: [{:.2f}..{:.2f}]'.format(np.min(weight_females), np.max(height_females)))
    print('Weight mean: {:.2f}'.format(np.mean(weight_females)))
    print('Weight std: {:.2f}'.format(np.std(weight_females)))

    print()

    print('*** Males Summary ***')
    print('Height range: [{:.2f}..{:.2f}]'.format(np.min(height_males), np.max(height_males)))
    print('Height mean: {:.2f}'.format(np.mean(height_males)))
    print('Height std: {:.2f}'.format(np.std(height_males)))
    print('Weight range: [{:.2f}..{:.2f}]'.format(np.min(weight_males), np.max(height_males)))
    print('Weight mean: {:.2f}'.format(np.mean(weight_males)))  
    print('Weight std: {:.2f}'.format(np.std(weight_males)))        