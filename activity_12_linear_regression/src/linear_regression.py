# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: correlation analysis and linear regression (attempt)

from google.colab import drive
import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# definitions/parameters
DATA_FOLDER = '/content/drive/MyDrive/Colab Datasets/country_indicators/'
DATASET_NAME = 'country_indicators.csv'

# Google drive mount
drive.mount('/content/drive')

# TODO: create a pandas data frame from the CSV file

# (optional) TODO: define the country as the index for the data frame

# (optional) TODO: remove all columns except 'gdp_per_capita' and 'life_expectacy' from the data frame

# TODO: remove any country (index) that does not have both 'gdp_per_capita' and 'life_expectancy' values

# TODO: compute and display the correlation matrix between 'gdp_per_capita' and 'life_expectancy'

# TODO: attempt a linear regression model, displaying the obtained r2 score

# TODO: produce a visualization of the data points and the fitted line
