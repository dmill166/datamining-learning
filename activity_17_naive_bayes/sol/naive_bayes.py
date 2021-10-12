# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 17: Naive Bayes Classification

import os, math, sys
import pandas as pd
from pandas.core.frame import DataFrame
from scipy.stats import norm
from sklearn.naive_bayes import GaussianNB

# definitions/parameters
DATA_FOLDER = '../data'
CSV_FILE_NAME   = 'realestate.csv'

if __name__ == "__main__":

    # TODOd: read the CSV file as a dataframe
    df = pd.read_csv(os.path.join(DATA_FOLDER, CSV_FILE_NAME))
    # print(df)

    # TODO: for each attribute, estimate the normal distribution parameters

    # TODOd: get all "target" classes (eg: [0, 1, 2, 3, 4])
    classes = df.iloc[:,-1].unique()
    classes.sort()
    #print(classes)

    # TODOd: get name of the target class (eg: bedrooms)
    target_class = df.columns[-1]
    print(target_class)

    # TODO: classify each row using naive bayes, computing the accuracy
    correct = 0
    for _, row in df.iterrows():
        probs = [1] * len(classes)
        for _class in classes:
            # probability of the class
            total_class = len(df[df[target_class] == _class])
            p_class = total_class / len(df)
            # print(_class, p_class)
            for col in df.columns[:-1]:
                probs[_class] *= len(df[(df[col] == row[col]) & (df[target_class] == _class)]) / total_class
            probs[_class] *= p_class
        print(probs)
        break



    # TODO: repeat but now use the scikit learn classifier