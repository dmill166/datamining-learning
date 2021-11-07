# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 20: ANN for the real estate dataset
import pandas as pd
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
import numpy as np


def min_max(data, interval=(0, 1)):
    return [(v - min(data)) / (max(data) - min(data)) * (interval[1] - interval[0]) + interval[0] for v in data]


if __name__ == "__main__":
    real_estate_dataset = [
        [1, 30000, 0, 1, 0],
        [2, 50000, 0, 1, 2],
        [4, 70000, 1, 3, 3],
        [6, 90000, 1, 3, 3],
        [2, 55000, 1, 2, 0],
        [4, 55000, 1, 2, 3],
        [3, 60000, 1, 2, 2],
        [1, 35000, 0, 1, 2],
        [1, 25000, 0, 2, 1],
        [6, 95000, 1, 3, 4],
        [6, 85000, 1, 4, 4],
        [4, 50000, 1, 3, 3],
        [3, 50000, 0, 3, 3],
        [4, 80000, 1, 3, 2],
        [6, 90000, 1, 2, 4],
        [4, 75000, 1, 3, 4],
        [2, 60000, 1, 2, 1]
    ]
    df = pd.DataFrame(real_estate_dataset)
    data = np.array(real_estate_dataset, dtype="float")
    # TODO: normalize attribute values first
    min_max_scaler = preprocessing.MinMaxScaler()
    print(df)
    data = pd.DataFrame(min_max_scaler.fit_transform(df))
    print(data)

    # TODO: train a multilayer ANN to implement a real estate classifier
    X = data.iloc[:, :-1]
    Y = data.iloc[:, -1]
    clf = MLPClassifier(random_state=0).fit(X, Y)

    # TODO: compute the accuracy of the classifier
