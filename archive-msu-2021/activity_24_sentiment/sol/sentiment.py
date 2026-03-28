# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 24: Illustrates Sentiment Analysis

from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.corpus import words
from nltk.tokenize import word_tokenize
import csv, os, string
import matplotlib.pyplot as plt 

DATA_FOLDER = "../data"
TWEETS_FILE = "tweets.csv"

if __name__ == "__main__":

    # TODO: evaluate the sentiment of all tweets from the dataset 
    tokenizer = PunktSentenceTokenizer()
    sia = SentimentIntensityAnalyzer()
    sentiment = []
    with open(os.path.join(DATA_FOLDER, TWEETS_FILE), "rt") as tweets_file:
        reader = csv.reader(tweets_file)
        for row in reader:
            text = row[2]
            sentences = tokenizer.tokenize(text)
            for sentence in sentences:
                score = sia.polarity_scores(sentence)["compound"]
                sentiment.append(score)
                if score > .75:
                    print(sentence)

    # TODO: produce a boxplot of the sentiment polarity considering all tweets  
    plt.boxplot(sentiment, vert=False)
    plt.xlabel("Sentiment Polarity")

    plt.show()
