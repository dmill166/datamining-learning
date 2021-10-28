# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 21: ANN for hearts and diabetes datasets

from sklearn.neural_network import MLPClassifier 
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
import random, os
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

# definitions/parameters
DATA_FOLDER = '../data'
CSV_FILE_NAME   = 'heart.csv'

if __name__ == "__main__":
  
  # TODO: split the dataset into training and test dataset (assume the training set is 20% of the whole dataset)
  df = pd.read_csv(os.path.join(DATA_FOLDER, CSV_FILE_NAME))
  df_train, df_test = train_test_split(df, test_size=0.2, random_state=0)

  # TODO: normalize attribute values first  
  min_max_scaler = preprocessing.MinMaxScaler()
  X_train = min_max_scaler.fit_transform(df_train.iloc[:,:-1].values)
  X_test = min_max_scaler.fit_transform(df_test.iloc[:,:-1].values)
  # X_test = df_test.iloc[:,:-1].values
  Y_train = df_train.iloc[:,-1].values
  Y_test = df_test.iloc[:,-1].values

  # TODO: train a multilayer ANN to implement a hearts (disease) classifier
  clf = MLPClassifier(hidden_layer_sizes=(6,3), max_iter=3000, random_state=0)
  clf.fit(X_train, Y_train)

  # TODO: compute the accuracy of the classifier
  print('Accuracy:', clf.score(X_test, Y_test))