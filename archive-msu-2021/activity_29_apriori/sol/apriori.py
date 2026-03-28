# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 29: Apriori

import os, csv, json, sys
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import pandas as pd

# defintions/parameters
DATA_FOLDER      = '../data/'
DATASET_CSV_FILE = 'retail.csv'
MIN_SUP          = .005

if __name__ == "__main__":

    # TODO: read dataset
    print('reading dataset...')
    # dataset = []
    # with open(os.path.join(DATA_FOLDER, DATASET_CSV_FILE), encoding='utf-8') as csv_file:
    #     reader = csv.reader(csv_file)
    #     current_id = None
    #     for row in reader:
    #         id = row[0]
    #         item = row[1]
    #         item = item.encode('ascii', errors='ignore').decode('ascii')
    #         if not current_id:
    #             current_id = id 
    #             items = [item]
    #         elif current_id == id:
    #             items.append(item)
    #         else:
    #             dataset.append(items)
    #             current_id = id 
    #             items = [item]
    #     if current_id:
    #         dataset.append(items)
    # #print(dataset)
    # print('done!')
    df = pd.read_csv('../data/kaggle_groceries.csv')
    dataset = {}
    for _, row in df.iterrows():
        key = (row['Member_number'], row['Date'])
        if key not in dataset:
            dataset[key] = []
        dataset[key].append(row['itemDescription'])
    dataset = list(dataset.values())
    # print(dataset)
    
    # TODO: apply apriori algorithm using MLxtend
    te = TransactionEncoder()
    te_array = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_array, columns=te.columns_)
    # print(df)
    result = apriori(df, min_support=MIN_SUP, use_colnames=True)
    result = result[result['itemsets'].apply(lambda value: len(value) > 1)]
    print(result)

