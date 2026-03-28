# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: correlation analysis and linear regression (attempt)

# from google.colab import drive
import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME = 'country_indicators.csv'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, CSV_FILE_NAME)
# DATA_FOLDER = '/content/drive/MyDrive/Colab Datasets/country_indicators/'
# DATASET_NAME = 'country_indicators.csv'

# Google drive mount
# drive.mount('/content/drive')

if __name__ == "__main__":

# TODO: create a pandas data frame from the CSV file
# https://pandas.pydata.org/pandas-docs/stable/getting_started/intro_tutorials/02_read_write.html
    df = pd.read_csv(CSV_FILE_PATH)

# (optional) TODO: define the country as the index for the data frame
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html
    df.index = df['country'].values

# (optional) TODO: remove all columns except 'gdp_per_capita' and 'life_expectacy' from the data frame
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.drop.html
# https://www.geeksforgeeks.org/iterate-over-a-list-in-python/
# https://www.geeksforgeeks.org/how-to-get-column-names-in-pandas-dataframe/
    remove_list = [i for i in df.columns if i != 'gdp_per_capita' and i != 'life_expectancy']
    print("Dataframe columns:", len(df.columns))
    df = df.drop(columns=remove_list, axis=1)

# TODO: remove any country (index) that does not have both 'gdp_per_capita' and 'life_expectancy' values
    countries_to_drop = [country for country in df.index if (np.isnan(df.loc[country]['gdp_per_capita']) or np.isnan(df.loc[country]['life_expectancy']))]
    df = df.drop(index=countries_to_drop)

# TODO: compute and display the correlation matrix between 'gdp_per_capita' and 'life_expectancy'
# https://www.geeksforgeeks.org/how-to-create-a-correlation-matrix-using-pandas/
    corr = df.corr()
    print('*** Correlation Matrix ***')
    print(corr)

# TODO: attempt a linear regression model, displaying the obtained r2 score
    # linear regression
    X = df['gdp_per_capita'].values.reshape((-1, 1))
    Y = df['life_expectancy'].values.reshape((-1, 1))
    model = LinearRegression().fit(X, Y)
    score = model.score(X, Y)
    print('r2 scores: {:.2f}'.format(score))

# TODO: produce a visualization of the data points and the fitted line
    # visualization
    Y_pred = model.predict(X)
    plt.scatter(X, Y)


    for i in range(5):
        print("Done with program! x", i)
