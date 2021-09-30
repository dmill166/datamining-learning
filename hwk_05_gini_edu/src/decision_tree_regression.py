# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: correlation analysis and decision tree regression (attempt)

#from google.colab import drive
import pandas as pd
import numpy as np
import os
from sklearn.tree import DecisionTreeRegressor
import matplotlib.pyplot as plt

# definitions/parameters
DATA_FOLDER = '../data'
DATASET_NAME = 'country_indicators.csv'

# Google drive mount
# drive.mount('/content/drive')

# TODO: create a pandas data frame from the CSV file

# (optional) TODO: define the country as the index for the data frame

# (optional) TODO: remove all columns except 'gini' and 'edu_index' from the data frame

# TODO: remove any country (index) that does not have both 'gini' and 'edu_index' values

# TODO: compute and display the correlation matrix between 'gini' and 'edu_index'

# TODO: attempt a linear regression model, displaying the obtained r2 score

# TODO: produce a visualization of the data points and the fitted points
