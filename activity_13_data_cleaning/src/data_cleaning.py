# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 12: data cleaning

from google.colab import drive
import csv 
import os
import matplotlib.pyplot as plt 
import re
from datetime import datetime
import sys

# definitions/parameters
DATA_FOLDER = '/content/drive/MyDrive/Colab Datasets/orders_dataset'

# Google drive mount
drive.mount('/content/drive')

def clean_up(text): 
  text = re.sub('[^\w\s\-&]', '', text)
  return re.sub(' +', ' ', text).strip()

def capitalize(text):
    s = ''
    for word in text.split(' '):
        s += word.lower().capitalize() + ' '
    return s.strip()

if __name__ == "__main__":

  # TODO: parse items
  # for category, if 'music' replace with 'musical instruments', if 'appliance' replace with 'appliances', and if 'office' replace with 'office suplies'
  # make sure all descriptions, units, and categories are lower case/capitalized and only contain alphanumerical, the dash, and the ampersand characters
  items = {}

  # TODO: parse orders
  # make sure order# uses the format 99999-XX, where XX is a 2-letter in uppercase
  # if order# users the format 99999, assume XX = CO
  # datetime may appear in formats: %Y-%m-%d %H:%M:%S or %m/%d/%y %H:%M or %m/%d/%y %H:%M:%S
  # make sure all client names, addresses and cities are lower case/capitalized and only contain alphanumerical, the dash, and the ampersand characters
  # for state, make sure they use the format XX, where XX is a 2-letter in uppercase
  # if state is Texas, replace with TX
  # check for valid email format (when informed)
  # make sure item codes are valid (ie, item exists)
  orders = {}
          
  # display a line plot showing the total orders per month per state in the year 2021 
