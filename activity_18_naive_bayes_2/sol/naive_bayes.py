# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 18: Naive Bayes Classification

import os, math, sys, random
import pandas as pd
from pandas.core.frame import DataFrame
from sklearn.naive_bayes import GaussianNB

# definitions/parameters
DATA_FOLDER = '../data'
CSV_FILE_NAME   = 'heart.csv'

if __name__ == "__main__":

    # TODO: split the dataset into training and test dataset (assume the training set is 10% of the whole dataset)
    # make sure you select data rows randomly and without repetition
    df = pd.read_csv(os.path.join(DATA_FOLDER, 'diabetes.csv'))
    random.seed(0)
    rows_train = random.sample(range(len(df)), k=int(len(df) * .1))
    # print(rows_train)
    df_train = pd.DataFrame(columns=df.columns)
    df_test = pd.DataFrame(columns=df.columns)
    for i, row in df.iterrows():
        if i in rows_train:
            df_train = df_train.append(row)
        else:
            df_test = df_test.append(row)

    # TODO: for each attribute, estimate the normal distribution parameters

    # TODO: get all "target" classes (eg: [0, 1, 2, 3, 4])
    classes = df.iloc[:,-1].unique()
    classes.sort()

    # TODO: get name of the target class (eg: bedrooms)
    target_class = df.columns[-1]

    # TODO: classify each row using naive bayes, computing the accuracy

    # TODO: repeat but now use the scikit learn classifier
    X = df_train.iloc[:,0:-1].values
    Y = df_train.iloc[:,-1].values
    # print(Y)
    model = GaussianNB().fit(X, Y)
    correct = 0
    for _, row in df_test.iterrows():
        value_predict = model.predict([row[:-1].values])
        if value_predict == row[target_class]:
            correct += 1
    print('accuracy:', correct/len(df_test.index))