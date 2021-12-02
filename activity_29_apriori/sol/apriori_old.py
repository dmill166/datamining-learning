# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 29: Apriori

import os, csv, json, sys
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import pandas as pd

# defintions/parameters
DATA_FOLDER           = '../data/'
TRANSACTIONS_CSV_FILE = 'transactions.csv'
MIN_SUP_COUNT         = 2

if __name__ == "__main__":

    # read transactions 
    transactions = {}
    with open(os.path.join(DATA_FOLDER, TRANSACTIONS_CSV_FILE)) as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            id, item = row
            id = int(id)
            item = int(item)
            if id not in transactions:
                transactions[id] = []
            transactions[id].append(item)
    for id in transactions:
        print(id, transactions[id])

    # l1-itemsets
    l1_itemsets = {}
    for id in transactions:
        for item in transactions[id]:
            if item not in l1_itemsets:
                l1_itemsets[item] = 0
            l1_itemsets[item] += 1
    l1_itemsets = [(k, v) for k, v in l1_itemsets.items()]
    l1_itemsets = sorted(list(l1_itemsets), key = lambda tuple: tuple[0])
    print('l1_itemsets:')
    print(l1_itemsets)

    # l2-itemsets
    l2_itemsets = {}    
    for item_a, _ in l1_itemsets:
        for item_b, _ in l1_itemsets:
            if item_a < item_b:
                for id in transactions:
                    if item_a in transactions[id] and item_b in transactions[id]:
                        if (item_a, item_b) not in l2_itemsets:
                            l2_itemsets[(item_a, item_b)] = 0
                        l2_itemsets[(item_a, item_b)] += 1
    print('l2_itemsets:')
    print(l2_itemsets)
    l2_itemsets_new = {}
    for key in l2_itemsets:
        if l2_itemsets[key] >= MIN_SUP_COUNT:
            l2_itemsets_new[key] = l2_itemsets[key]
    l2_itemsets = l2_itemsets_new
    print('l2_itemsets:')
    print(l2_itemsets)

    # l3-itemsets
    l3_itemsets = {}    
    for item_a in l2_itemsets:
        for item_b in l2_itemsets:
            key = tuple(set(item_a).union(set(item_b)))
            if len(key) != 3:
                continue
            if key in l3_itemsets:
                continue
            for id in transactions:
                all_in = True 
                for item in key:
                    if item not in transactions[id]:
                        all_in = False
                        break
                if all_in:
                    if key not in l3_itemsets:
                        l3_itemsets[key] = 0
                    l3_itemsets[key] += 1
    print(l3_itemsets)

    # apriori using MLxtend
    dataset = []
    for id in transactions:
        dataset.append(transactions[id])
    print(dataset)
    te = TransactionEncoder()
    te_array = te.fit(dataset).transform(dataset)
    df = pd.DataFrame(te_array, columns=te.columns_)
    print(df)
    result = apriori(df, min_support=0.25, use_colnames=True)
    print(result)

