# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Homework 08: State of the Union

import string, operator
import nltk, csv, os
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# definitions/parameters
DATA_FOLDER = '../data'
FILE_NAME   = '2014.txt' # pick one state of the union file

# returns the indices of the top n values of a numpy array
def top_indices(data, n):
  return data.argsort()[-1*n:][::-1]

if __name__ == "__main__":

    # this was given to you (enjoy)
    state_union = ""
    with open(os.path.join(DATA_FOLDER, FILE_NAME), 'rt') as file:
        for line in file:
            state_union += line + "\n"
    
    # TODO: extract the sentences from state_union


    # TODO: extract a bag of bigrams from the previous sentences


    # TODO: using LDA, extract the top 5 topics from the previous bag of bigrams
