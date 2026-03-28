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
df = pd.read_csv(os.path.join(DATA_FOLDER, DATASET_NAME))

# (optional) TODO: define the country as the index for the data frame
df.index = df['country'].values

# (optional) TODO: remove all columns except 'gdp_per_capita' and 'life_expectacy' from the data frame
columns_to_drop = [ column for column in df.columns if column != 'gdp_per_capita' and column != 'life_expectancy' ]
df = df.drop(columns=columns_to_drop)

# TODO: remove any country (index) that does not have both 'gdp_per_capita' and 'life_expectancy' values
countries_to_drop = [ country for country in df.index if np.isnan(df.loc[country]['gdp_per_capita']) or np.isnan(df.loc[country]['life_expectancy']) ]
df = df.drop(index=countries_to_drop)

# TODO: compute and display the correlation matrix between 'gdp_per_capita' and 'life_expectancy'
corr = df.corr()
print('*** Correlation Matrix ***')
print(corr)

# TODO: attempt a linear regression model, displaying the obtained r2 score
X = df['gdp_per_capita'].values.reshape((-1, 1))
Y = df['life_expectancy'].values.reshape((-1, 1))
model = LinearRegression().fit(X, Y)
score = model.score(X, Y)
print('r2 score: {:.2f}'.format(score))

# TODO: produce a visualization of the data points and the fitted line
Y_pred = model.predict(X)
plt.scatter(X, Y)
plt.plot(X, Y_pred, '-r')
plt.xlabel('GDP per capita')
plt.ylabel('Life Expectancy')
plt.show()