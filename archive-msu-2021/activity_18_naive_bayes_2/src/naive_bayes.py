# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 18: Naive Bayes Classification

import os, math, sys, random
import pandas as pd
from pandas.core.frame import DataFrame
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn import tree

# definitions/parameters
DATA_FOLDER = '../data'
CSV_FILE_NAME   = 'heart.csv'

if __name__ == "__main__":

    # TODO: split the dataset into training and test dataset (assume the training set is 10% of the whole dataset)
    # make sure you select data rows randomly and without repetition
    
    # TODO: for each attribute, estimate the normal distribution parameters

    # TODO: get all "target" classes (eg: [0, 1, 2, 3, 4])

    # TODO: get name of the target class (eg: bedrooms)

    # TODO: classify each row using naive bayes, computing the accuracy

    # TODO: repeat but now use the scikit learn classifier