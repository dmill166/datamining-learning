# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 22: Illustrates NLKT

import nltk, string
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.tokenize.punkt import PunktSentenceTokenizer

from nltk.stem import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import SnowballStemmer

from nltk.stem import WordNetLemmatizer

from nltk import ne_chunk
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import requests 
import os

# definitions/parameters
GUTENBERG_URL = "https://www.gutenberg.org/files/1342/1342-0.txt"
DATA_FOLDER = "../data"
OUTPUT_FILE = "word_tokens.txt"

if __name__ == "__main__":

    # TODO: obtain the raw text as a string
    result = requests.get(GUTENBERG_URL)
    raw_text = result.content.decode("utf-8")
    # print(raw_text)

    # TODO: extract word tokens from raw text
    word_tokens = word_tokenize(raw_text)
    stop_words = stopwords.words("english")
    word_tokens_no_stop_words = [ token.lower() for token in word_tokens if token not in stop_words and token not in string.punctuation]
    # print(word_tokens_no_stop_words)

    # TODO: extract sentence tokens from raw text
    sent_tokens = sent_tokenize(raw_text)
    # print(sent_tokens)

    # TODO: count how many times the word "love" appears
    # TODO: save all tokens in a text file (one word token per line)
    with open(os.path.join(DATA_FOLDER, OUTPUT_FILE), "wt") as output:
        love_freq = 0
        for token in word_tokens_no_stop_words:
            output.write(token + "\n")
            if token.lower() == 'love':
                love_freq += 1
        print(f"The word 'love' appeared {love_freq} times in the book")

    # TODO: POS taggging
    pos_tags = nltk.pos_tag(word_tokens_no_stop_words)
    # print(pos_tags)

    # TODO: show only nouns
    nouns = []
    for token, tag in pos_tags:
        if tag.startswith("NN"):
            nouns.append(token)
    #print(nouns)

    # TODO: for each of the nouns, show its stem and lemma
    ss = SnowballStemmer("english")
    wn = WordNetLemmatizer()
    for noun in nouns:
        print(f"{noun}, {ss.stem(noun)}, {wn.lemmatize(noun)}")

    # TODO: perform a NER tagging

    # TODO: compute a bag of words for each sentence, create a dictionary associating a word and its frequency, sort it by frequency (descending order)

    # TODO: do the same but for bigrams