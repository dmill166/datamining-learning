# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Homework 08: State of the Union
# Resources
#   https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed
#   https://stackoverflow.com/questions/37651057/generate-bigrams-with-nltk
import operator

import nltk
import os

# definitions/parameters
from nltk import sent_tokenize
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

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
    sent_tokens = nltk.sent_tokenize(state_union)
    print(sent_tokens)
    print()

    # TODO: extract a bag of bigrams from the previous sentences
    sent_tokens = sent_tokenize(state_union)
    count_vect = CountVectorizer(stop_words="english", ngram_range=(2, 2))
    bag_of_bigrams = count_vect.fit_transform(sent_tokens).toarray()
    bigrams = count_vect.get_feature_names()
    bigrams_freq = {}
    for row in bag_of_bigrams:
        for i in range(len(row)):
            bigram = bigrams[i]
            if bigram not in bigrams_freq:
                bigrams_freq[bigram] = 0
            bigrams_freq[bigram] += row[i]
    bigrams_freq = sorted(bigrams_freq.items(), key=lambda item: item[1], reverse=True)
    print('Top 10 bigrams found:')
    for i in range(10):
        print(bigrams_freq[i])
    print()

    # TODO: using LDA, extract the top 5 topics from the previous bag of bigrams
    lda = LatentDirichletAllocation(n_components=5, random_state=0)
    lda.fit(bag_of_bigrams)
    print('Top topics found:')
    for i, topic in enumerate(lda.components_):
        print("Topic", i+1, ", ".join(bigrams[j] for j in top_indices(topic, 5)))
