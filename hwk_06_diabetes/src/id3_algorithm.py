# CS390Z - Introduction to Data Mining - Fall 2021
# Instructor: Thyago Mota
# Description: Homework 06: ID3 algorithm (for decision trees)

import matplotlib.pyplot as plt
import os
import pandas as pd
import random
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import export_text

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME = 'diabetes.csv'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, CSV_FILE_NAME)


# Resources
# Utilized the following with printing a SKLearn Decision Tree
#   https://scikit-learn.org/stable/modules/tree.html
#   https://mljar.com/blog/visualize-decision-tree/
#   https://www.geeksforgeeks.org/how-to-get-column-names-in-pandas-dataframe/
# Confirmed how to add points to a matplotlib plot
#   https://stackoverflow.com/questions/44813601/how-to-set-x-axis-values-in-matplotlib-python


if __name__ == "__main__":

    df = pd.read_csv(CSV_FILE_PATH)
    runs = [x for x in range(10, 21)]
    accuracies = []

    for run in runs:
        print('run:', run)

        # TODO: split the dataset into training and test dataset
        # make sure you select data rows randomly and without repetition
        random.seed(8675309)
        rows_train = random.sample(range(len(df)), k=int(len(df) * .1))
        training_data = pd.DataFrame(columns=df.columns)
        test_data = pd.DataFrame(columns=df.columns)
        for i, row in df.iterrows():
            if i in rows_train:
                training_data = training_data.append(row)
            else:
                test_data = test_data.append(row)

        # TODO: train a decision tree model (you can use the id3 function or scikit learn)
        print('training...')
        X = training_data.iloc[:, 0:-1].values
        Y = training_data.iloc[:, -1].values
        model = DecisionTreeClassifier().fit(X, Y)

        # TODO: (optional) print the obtained decision tree
        print(export_text(model, feature_names=list(training_data.columns[:-1])))

        # TODO: compute the accuracy of the obtained model using the test dataset
        correct = 0.0
        for _, row in test_data.iterrows():
            value_predict = model.predict([row[:-1].values])
            if value_predict == row['target']:
                correct += 1.0
        denom = len(test_data.index)
        print('accuracy:', correct / denom)
        accuracies.append(correct / len(test_data.index))

    # TODO: plot learning curve

    plt.xlabel('Training Set %')
    plt.ylabel('Model\'s Accuracy')
    plt.plot(runs, accuracies, marker='o', linestyle='--', color='r',
             label='Square')
    plt.show()
