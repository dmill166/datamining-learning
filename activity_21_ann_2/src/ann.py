# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 21: ANN for hearts and diabetes datasets

from sklearn.neural_network import MLPClassifier 
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
import random, os
from sklearn.model_selection import train_test_split

# definitions/parameters
DATA_FOLDER = '../data'
CSV_FILE_NAME   = 'hearts.csv'

def min_max(data, interval=(0,1)):
  return [ (v - min(data)) / (max(data) - min(data)) * (interval[1] - interval[0]) + interval[0] for v in data ]

if __name__ == "__main__":

    # TODO: normalize attribute values first     


    # TODO: split the dataset into training and test dataset (assume the training set is 10% of the whole dataset)

    # TODO: train a multilayer ANN to implement a hearts (disease) classifier

    # TODO: compute the accuracy of the classifier
