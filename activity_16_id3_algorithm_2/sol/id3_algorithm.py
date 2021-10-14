# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 16: ID3 algorithm (for decision trees)

import os, math, sys, random
import pandas as pd
from pandas.core.frame import DataFrame
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn import tree

# definitions/parameters
# DATA_FOLDER     = '/content/drive/MyDrive/Colab Datasets/human_resources'
original_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME = 'heart.csv'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, CSV_FILE_NAME)


class DTree:

    def __init__(self, attribute='', value=0):
        self.attribute = attribute
        self.value = value
        self.left = None
        self.right = None

    def get_str(self, tabs):
        s = tabs + '[' + self.attribute + ',' + str(self.value) + ']'
        tabs += '   '
        if self.left:
            s += '\n' + self.left.get_str(tabs)
        if self.right:
            s += '\n' + self.right.get_str(tabs)
        return s

    def __str__(self):
        return self.get_str('')

    def predict(self, row, target):
        if self.attribute == target:
            return self.value
        value = row[self.attribute]
        if value <= self.value:
            return self.left.predict(row, target)
        else:
            return self.right.predict(row, target)


# computes the entropy given a data frame
def entropy(df):
    target_column = df.iloc[:, -1]
    target_counts = target_column.value_counts()
    total = len(df.index)
    entropy = [(-1) * (count / total) * math.log(count / total) for count in target_counts]
    return sum(entropy)


# computes a dedision tree given a data frame
# assumes that the last column is the target
def id3(df):
    # create a tree node
    tree = DTree()

    # if all target values are the same (zero entropy), then return a tree with the target value
    if entropy(df) == 0:
        tree.attribute = df.columns[-1]
        tree.value = df.iloc[0, -1]
        return tree

    # if the dataframe does not have attributes (other than the target), then return a tree with the most common target
    if len(df.columns) == 1:
        tree.attribute = df.columns[-1]
        target_column = df.iloc[:, -1]
        target_counts = target_column.value_counts()
        for i in target_counts.index:
            if target_counts[i] == max(target_counts):
                tree.value = i
                return tree

                # all other cases
    current_entropy = entropy(df)
    best_info_gain = -1
    best_attribute = None
    best_value = -1
    left_df = DataFrame()
    right_df = DataFrame()
    for candidate_attribute in df.columns[:-1]:
        selection = df[candidate_attribute]
        for candidate_value in selection.unique():
            temp_left_df = DataFrame()
            temp_right_df = DataFrame()
            for _, row in df.iterrows():
                value = row[candidate_attribute]
                if value <= candidate_value:
                    temp_left_df = temp_left_df.append(row, ignore_index=True)
                else:
                    temp_right_df = temp_right_df.append(row, ignore_index=True)

            if len(temp_left_df.index) == 0 or len(temp_right_df.index) == 0:
                continue

            candidate_info_gain = current_entropy - entropy(temp_left_df) * len(temp_left_df.index) / len(
                df.index) - entropy(temp_right_df) * len(temp_right_df.index) / len(df.index)
            if candidate_info_gain > best_info_gain:
                best_attribute = candidate_attribute
                best_value = candidate_value
                best_info_gain = candidate_info_gain
                left_df = temp_left_df
                left_df = left_df.drop(columns=[candidate_attribute])
                right_df = temp_right_df
                right_df = right_df.drop(columns=[candidate_attribute])

    # if any of the split tree is empty, then return a tree with the most common target
    if len(left_df.index) == 0 or len(right_df.index) == 0:
        tree.attribute = df.columns[-1]
        target_column = df.iloc[:, -1]
        target_counts = target_column.value_counts()
        for i in target_counts.index:
            if target_counts[i] == max(target_counts):
                tree.value = i
                return tree

                # recursive calls id3 to the left and to the right
    tree.attribute = best_attribute
    tree.value = best_value
    tree.left = id3(left_df)
    tree.right = id3(right_df)

    # return the tree
    return tree


if __name__ == "__main__":

    # TODOd: split the dataset into training and test dataset (assume the training set is 10% of the whole dataset)
    # make sure you select data rows randomly and without repetition
    random.seed(0)
    df = pd.read_csv(CSV_FILE_PATH)
    rows_train = random.sample(range(len(df)), k=int(len(df) * .2))
    # print(rows_train)
    df_train = pd.DataFrame(columns=df.columns)
    df_test = pd.DataFrame(columns=df.columns)
    for i, row in df.iterrows():
        if i in rows_train:
            df_train = df_train.append(row)
        else:
            df_test = df_test.append(row)

    # print(len(df_train))
    # print(len(df_test))

    # TODO: call id3 on the training dataset
    df_train = pd.read_csv(CSV_FILE_PATH)
    my_tree = id3(df_train)

    # TODO; print the obtained decision tree
    print(my_tree)

    # TODO: compute the accuracy of the decision tree using the test dataset
    correct = 0
    df_test = pd.read_csv(CSV_FILE_PATH)
    for _, row in df_test.iterrows():
        value_predict = my_tree.predict(row, 'target')
        if value_predict == row['target']:
            correct += 1
    print('accuracy:', correct / len(df_test.index))

    # TODO: do the same but now using sklearn's DecisionTreeClassifier
    X = df_train.iloc[:, 0:-1].values
    Y = df_train.iloc[:, -1].values
    model = DecisionTreeClassifier().fit(X, Y)
    print(export_text(model, feature_names=list(df_train.columns[:-1])))

    correct = 0
    for _, row in df_test.iterrows():
        value_predict = model.predict([row[:-1].values])
        if value_predict == row['target']:
            correct += 1
    print('accuracy:', correct / len(df_test.index))
