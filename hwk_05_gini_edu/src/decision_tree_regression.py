# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: correlation analysis and decision tree regression (attempt)

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME = 'country_indicators.csv'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, CSV_FILE_NAME)

if __name__ == "__main__":

    # TODO: create a pandas data frame from the CSV file
    df = pd.read_csv(CSV_FILE_PATH)
    print(df)

    # (optional) TODO: define the country as the index for the data frame
    df.index = df['country'].values

    # (optional) TODO: remove all columns except 'gini' and 'edu_index' from the data frame
    columns_to_drop = [column for column in df.columns if column != 'gini' and column != 'edu_index']
    df = df.drop(columns=columns_to_drop)

    # TODO: remove any country (index) that does not have both 'gini' and 'edu_index' values
    countries_to_drop = [country for country in df.index if np.isnan(df.loc[country]['gini'])
                         or np.isnan(df.loc[country]['edu_index'])]
    df = df.drop(index=countries_to_drop)

    # TODO: compute and display the correlation matrix between 'gini' and 'edu_index'
    corr = df.corr()
    print('*** Correlation Matrix ***')
    print(corr)

# TODO: attempt a linear regression model, displaying the obtained r2 score

# TODO: produce a visualization of the data points and the fitted points
