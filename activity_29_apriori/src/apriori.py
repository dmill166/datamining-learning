# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 29: Apriori

import os, csv, json, sys
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
import pandas as pd

# defintions/parameters
DATA_FOLDER      = '../data/'
DATASET_CSV_FILE = 'groceries.csv'
MIN_SUP          = .6

if __name__ == "__main__":

    # TODO: read dataset
    
    
    # TODO: apply apriori algorithm using MLxtend


