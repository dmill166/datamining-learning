# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 22: Illustrates NLKT

# pip3 install nltk
import nltk
from nltk.corpus import stopwords

# required modules for tokenization
from nltk.tokenize import word_tokenize, sent_tokenize

# required modules for stemming and lemmanization
from nltk.stem import SnowballStemmer
from nltk.stem import WordNetLemmatizer

# required modules for NER
from nltk import ne_chunk
from nltk.tree import Tree

# required modules for bag of words
import operator
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

import requests 
import os

# definitions/parameters
GUTENBERG_URL = "https://www.gutenberg.org/files/1342/1342-0.txt"
DATA_FOLDER = "../data"
OUTPUT_FILE = "word_tokens.txt"

# extract the NER from a tree
def extract_ner_tags(ner_tree, label=None):
  for node in ner_tree:
    if hasattr(node, 'label'):
      if not label or node.label() == label:
        yield node
    elif type(node) == Tree:
      extract_ner_tags(node, label)

if __name__ == "__main__":

    # TODO: obtain the raw text as a string
    result = requests.get(GUTENBERG_URL)
    raw_text = result.content.decode("utf-8")

    # *** Technique #1: TOKENIZATION ***
    print("*** Technique #1: TOKENIZATION ***")

    # TODO: extract word tokens from raw text
    word_tokens = word_tokenize(raw_text)
    #print("word tokens", word_tokens)

    # TODO: extract sentence tokens from raw text
    sent_tokens = sent_tokenize(raw_text)
    #print("sentence tokens", sent_tokens)

    # TODO: count how many time the word "love" appears
    # TODO: save all tokens in a text file (one word token per line)
    with open(os.path.join(DATA_FOLDER, OUTPUT_FILE), "wt") as output:
        love_freq = 0
        for token in word_tokens:
            output.write(token + "\n")
            if token.lower() == 'love':
                love_freq += 1
        print(f"The word 'love' appeared {love_freq} times in the book")

    # *** Technique #2: Part of Speech (POS) Tagging ***
    print("*** Technique #2: Part of Speech (POS) Tagging ***")    

    # TODO: POS taggging
    pos_tags = nltk.pos_tag(word_tokens)
    # print(pos_tags)

    # *** Technique #3: Stemming and Lemmanization ***
    print("*** Technique #3: Stemming and Lemmanization ***")

    # TODO: show only nouns
    # TODO: for each of the nouns, show its stem and lemma
    # print()
    # print("Nouns found in the book (and their stems):")
    # sbs = SnowballStemmer("english")
    # wl = WordNetLemmatizer()
    # for word, tag in pos_tags:
    #   if tag.startswith("NN"):
    #     stem = sbs.stem(word)
    #     lemma = wl.lemmatize(word)
    #     print(word, "-", stem, "-", lemma)
    # print()

    # *** Technique #4: Named Entity Recognition (NER) ***
    print("*** Technique #4: Named Entity Recognition (NER) ***")

    # TODO: perform a NER tagging
    ner_tree = ne_chunk(pos_tags)
    people = []
    print("People found in the book:")
    for node in extract_ner_tags(ner_tree, label='PERSON'):
      person = ""
      for word, _ in node.leaves():
        person += word + " "
      person = person.strip()
      if person not in people:
        people.append(person)
    print(people)

    # *** Technique #5: Bag of Words ***
    print("*** Technique #5: Bag of Words ***")

    # # TODO: compute a bag of words for each sentence, create a dictionary associating a word and its frequency, sort it by frequency (descending order)
    count_vect = CountVectorizer(stop_words="english")
    count_data = count_vect.fit_transform(sent_tokens).toarray()
    # print(count_data)
    words = count_vect.get_feature_names()
    words_freq = {}
    for row in count_data:
      for i in range(len(row)):
        word = words[i]
        if word not in words_freq:
          words_freq[word] = 0
        words_freq[word] += row[i]
    words_freq = sorted(words_freq.items(), key=operator.itemgetter(1), reverse=True)
    print("Top 10 words found in text:")
    for i in range(10):
      print(words_freq[i])

    # TODO: do the same but for bigrams
    count_vect = CountVectorizer(stop_words="english", ngram_range=(2,2))
    count_data = count_vect.fit_transform(sent_tokens).toarray()
    # print(count_data)
    bigrams = count_vect.get_feature_names()
    bigrams_freq = {}
    for row in count_data:
      for i in range(len(row)):
        bigram = bigrams[i]
        if bigram not in bigrams_freq:
          bigrams_freq[bigram] = 0
        bigrams_freq[bigram] += row[i]
    bigrams_freq = sorted(bigrams_freq.items(), key=operator.itemgetter(1), reverse=True)
    print("Top 10 bigrams found in text:")
    for i in range(10):
      print(bigrams_freq[i])