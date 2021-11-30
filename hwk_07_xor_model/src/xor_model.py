# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Homework 07: XOR ANN 

from sklearn.neural_network import MLPClassifier 
import numpy as np

if __name__ == "__main__":

    xor_dataset = [ 
        [1, -1, -1, -1], 
        [1, 1, -1, 1],
        [1, -1, 1, 1],
        [1, 1, 1, -1]
    ]
    array = np.array(xor_dataset)

    # TODO: train a MLP Classifier to implement a XOR classifier with only 1 hidden layer with 2 nodes
    X = array[0:, :-1]
    Y = array[0:, -1]
    clf = MLPClassifier(hidden_layer_sizes=2, max_iter=3000, random_state=0).fit(X, Y)

    # TODO: get the weights (coefs_ attribute)
    weights = clf.coefs_

    # TODO: get the biases (intercepts_ attribute)
    biases = clf.intercepts_

    # TODO: print the score
    clf.score(X, Y)


    # check the output
    w_01 = weights[0][0][0] 
    print("w_01:", w_01)
    w_02 = weights[0][0][1]
    print("w_02:", w_02)
    w_11 = weights[0][1][0]
    print("w_11:", w_11)
    w_12 = weights[0][1][1]
    print("w_12:", w_12)
    w_21 = weights[0][2][0]
    print("w_21:", w_21)
    w_22 = weights[0][2][1]
    print("w_22:", w_22)
    w_1out = weights[1][0][0]
    print("w_1out:", w_1out)
    w_2out = weights[1][1][0]
    print("w_2out:", w_2out)

    b_1 = biases[0][0]
    print("b_1:", b_1)
    b_2 = biases[0][1]
    print("b_2:", b_2)
    b_3 = biases[1][0]
    print("b_3:", b_3)

    x_0 = 1
    x_1 = -1 # FALSE
    x_2 = -1 # FALSE
    h_1 = max(x_0*w_01 + x_1*w_11 + x_2*w_21 + b_1, 0)
    h_2 = max(x_0*w_02 + x_1*w_12 + x_2*w_22 + b_2, 0)
    out = h_1*w_1out + h_2*w_2out + b_3
    print("x_1:", x_1, ", x_2:", x_2, ", out:", out)  

    x_1 = -1 # FALSE
    x_2 = 1 # TRUE
    h_1 = max(x_0*w_01 + x_1*w_11 + x_2*w_21 + b_1, 0)
    h_2 = max(x_0*w_02 + x_1*w_12 + x_2*w_22 + b_2, 0)
    out = h_1*w_1out + h_2*w_2out + b_3
    print("x_1:", x_1, ", x_2:", x_2, ", out:", out)  

    x_1 = 1 # TRUE
    x_2 = -1 # FALSE
    h_1 = max(x_0*w_01 + x_1*w_11 + x_2*w_21 + b_1, 0)
    h_2 = max(x_0*w_02 + x_1*w_12 + x_2*w_22 + b_2, 0)
    out = h_1*w_1out + h_2*w_2out + b_3
    print("x_1:", x_1, ", x_2:", x_2, ", out:", out)  

    x_1 = 1 # TRUE
    x_2 = 1 # TRUE
    h_1 = max(x_0*w_01 + x_1*w_11 + x_2*w_21 + b_1, 0)
    h_2 = max(x_0*w_02 + x_1*w_12 + x_2*w_22 + b_2, 0)
    out = h_1*w_1out + h_2*w_2out + b_3
    print("x_1:", x_1, ", x_2:", x_2, ", out:", out)  

