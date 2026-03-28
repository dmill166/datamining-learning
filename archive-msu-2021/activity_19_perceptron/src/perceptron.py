# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 19: AND/OR Perceptrons 

from sklearn.linear_model import Perceptron
import numpy as np

if __name__ == "__main__":

    and_dataset = [ 
        [1, -1, -1, -1], 
        [1, -1, 1, -1],
        [1, 1, -1, -1],
        [1, 1, 1, 1]
    ]
    #array = np.array(and_dataset)

    or_dataset = [ 
        [1, -1, -1, -1], 
        [1, -1, 1, 1],
        [1, 1, -1, 1],
        [1, 1, 1, 1]
    ]
    array = np.array(or_dataset)

    xor_dataset = [
        [1, -1, -1, -1],
        [1, -1, 1, 1],
        [1, 1, -1, 1],
        [1, 1, 1, -1]
    ]
    #array = np.array(or_dataset)

    # TODO: train a perceptron to implement AND/OR classifiers
    X = array[:, :-1]
    Y = array[:,-1]
    clf = Perceptron(random_state=0).fit(X, Y)
    print('Weights:', clf.coef_)
    print('Accuracy:', clf.score(X, Y))

    