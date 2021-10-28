# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Homework 07: XOR ANN 

from sklearn.neural_network import MLPClassifier 
import numpy as np

if __name__ == "__main__":

    xor_dataset = [ 
        [1, -1, -1, -1], 
        [1, -1, 1, 1],
        [1, 1, -1, 1],
        [1, 1, 1, -1]
    ]
    array = np.array(xor_dataset)

    # TODO: train a MLP Classifier to implement a XOR classifier with the minimum number of hidden layers and nodes possible
    

'''
x_0 = 1 (always)
x_1 = -1
x_2 = -1
out = ? 

h_1 = x_0w_01 + x_1w_11 + x_2w_21 
h_2 = x_0w_02 + x_1w_12 + x_2w_22

out = h_1w_1out + h_2w_2out 
'''

'''
x_0 = 1 (always)
x_1 = -1
x_2 = 1
out = ? 

h_1 = x_0w_01 + x_1w_11 + x_2w_21 
h_2 = x_0w_02 + x_1w_12 + x_2w_22

out = h_1w_1out + h_2w_2out 
'''

'''
x_0 = 1 (always)
x_1 = 1
x_2 = -1
out = ? 

h_1 = x_0w_01 + x_1w_11 + x_2w_21 
h_2 = x_0w_02 + x_1w_12 + x_2w_22

out = h_1w_1out + h_2w_2out 
'''

'''
x_0 = 1 (always)
x_1 = 1
x_2 = 1
out = ?

h_1 = x_0w_01 + x_1w_11 + x_2w_21 
h_2 = x_0w_02 + x_1w_12 + x_2w_22

out = h_1w_1out + h_2w_2out 
'''