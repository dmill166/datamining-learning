# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 24: Illustrates Sentiment Analysis

from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import words, subjectivity
from nltk.tokenize import word_tokenize
import nltk

nltk.download('subjectivity')
import csv, os, string
import pandas as pd

## Resources:
# Extract column from a dataframe
# https://towardsdatascience.com/extract-rows-columns-from-a-dataframe-in-python-r-678e5b6743d6

original_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
TWEETS_FILE = "tweets.csv"
TWEETS_FILE_PATH = os.path.join(DATA_FOLDER, TWEETS_FILE)

if __name__ == "__main__":
    # TODO: evaluate the sentiment of all tweets from the dataset
    df = pd.read_csv(TWEETS_FILE_PATH)
    tweets_list = list(df.iloc[:, 2])
    subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:len(tweets_list)]]
    obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:len(tweets_list)]]
    print(len(subj_docs), len(obj_docs))

    tokenizer = PunktSentenceTokenizer()
    sia = SentimentIntensityAnalyzer()

    # TODO: produce a boxplot of the sentiment polarity considering all tweets
