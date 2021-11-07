# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 21: ANN for the hearts and diabetes 

from sklearn.neural_network import MLPClassifier 
from sklearn import preprocessing
import pandas as pd
import numpy as np

if __name__ == "__main__":

    # TODO: get a dataframe from 

    # TODO: normalize attribute values first 
    df = pd.DataFrame(real_estate_dataset)
    min_max_scaler = preprocessing.MinMaxScaler()
    X = min_max_scaler.fit_transform(df.iloc[:,:-1].values)
    # print(X)

    # TODO: train a multilayer ANN to implement a real estate classifier
    Y = df.iloc[:,-1].values
    # print(Y)
    clf = MLPClassifier(hidden_layer_sizes=(100,25), max_iter=3000, random_state=0)
    clf.fit(X, Y)

    # TODO: compute the accuracy of the classifier
    print('Accuracy:', clf.score(X, Y))
