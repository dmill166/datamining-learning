# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 24: Illustrates Sentiment Analysis

from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import words
from nltk.tokenize import word_tokenize
import csv, os, string

DATA_FOLDER = "../data"
TWEETS_FILE = "tweets.csv"

if __name__ == "__main__":

    # TODO: evaluate the sentiment of all tweets from the dataset 

    # TODO: produce a boxplot of the sentiment polarity considering all tweets