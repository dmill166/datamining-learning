# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 17: Naive Bayes Classification

import os, math, sys
import pandas as pd
from pandas.core.frame import DataFrame
from scipy.stats import norm
from sklearn.naive_bayes import GaussianNB

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME   = 'realestate.csv'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, CSV_FILE_NAME)

if __name__ == "__main__":

    # TODO: read the CSV file as a dataframe
    df = pd.read_csv(CSV_FILE_PATH)
    print(df)

    # TODO: for each attribute, estimate the normal distribution parameters

    # TODO: get all "target" classes (eg: [0, 1, 2, 3, 4])
    classes = df.iloc[:,-1].unique()
    classes.sort()
    #print(classes)

    # TODO: get name of the target class (eg: bedrooms)
    target_class = df.columns[-1]
    print(target_class)

    # TODO: classify each row using naive bayes, computing the accuracy
    correct = 0
    for _, row in df.iterrows():
        probs = [0] * len(classes)
        # print(probs)
        for _class in classes:
            # probablity of the class
            total_class = len(df[df[target_class] == _class])
            p_class = total_class / len(df)
            for col in df.columns[:-1]:
                probs[_class] *= (len(df[(df[col] == row[col]) & df[target_class] == _class])) / total_class
        print(probs)

    # TODO: repeat but now use the scikit learn classifier
