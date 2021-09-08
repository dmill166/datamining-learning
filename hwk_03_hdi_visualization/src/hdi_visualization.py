# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Homework 03 - HDI Visualization

import os
import csv
import math
import matplotlib.pyplot as plt 

# definitions/parameters
DATA_FOLDER    = os.path.join('..', 'data')
HDI_FILE_NAME = 'hdi.csv'
TARGET_YEAR   = '2019'

if __name__ == "__main__":
    
    