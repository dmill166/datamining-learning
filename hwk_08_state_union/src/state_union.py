# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Homework 08: State of the Union
# Resources
#   https://linuxhint.com/extract_sentences_nltk_python_module/

import nltk
import os

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
    tokens = nltk.sent_tokenize(state_union)

    # TODO: extract a bag of bigrams from the previous sentences


    # TODO: using LDA, extract the top 5 topics from the previous bag of bigrams
