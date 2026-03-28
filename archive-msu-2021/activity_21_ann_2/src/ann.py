# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
<<<<<<< HEAD
# Description: Activity 20: ANN for the real estate dataset
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
=======
# Description: Activity 21: ANN for hearts and diabetes datasets

from sklearn.neural_network import MLPClassifier 
>>>>>>> f455a400bfe101e189f540b6c215ece5c1e4f36f
import numpy as np
import pandas as pd
from pandas.core.frame import DataFrame
import random, os
from sklearn.model_selection import train_test_split

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME = 'heart.csv'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, CSV_FILE_NAME)

def min_max(data, interval=(0,1)):
  return [ (v - min(data)) / (max(data) - min(data)) * (interval[1] - interval[0]) + interval[0] for v in data ]

if __name__ == "__main__":

  # TODO: normalize attribute values first
  min_max_scaler = preprocessing.MinMaxScaler()

  # TODO: split the dataset into training and test dataset (assume the training set is 10% of the whole dataset)
  df = pd.read_csv(CSV_FILE_PATH)
  df_train, df_test = train_test_split(df, test_size = 0.2)

  # TODO: train a multilayer ANN to implement a hearts (disease) classifier
  X_train = min_max_scaler.fit.transform(df_test.iloc[:, :-1].values)
  X_test = min_max_scaler.fit.transform(df_test)
  Y_train = df.train.iloc[:,-1].values
  Y_test = df_test.iloc[:,-1].values

  clf = MLPClassifier(hidden_layer_sizes=(6, 3), max_iter=3000, random_state=0)
  clf.fit(X_train, Y_train)

  # TODO: compute the accuracy of the classifier
  print('Accuracy:', clf.score(X_test, Y_test))
