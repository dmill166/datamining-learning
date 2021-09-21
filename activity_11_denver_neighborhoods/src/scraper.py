# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 11: a simple scraper

import csv 
import re 
import os
import requests
from bs4 import BeautifulSoup

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.abspath(''))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME = 'denver_neighborhoods.csv'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, CSV_FILE_NAME)
BASE_URL = 'https://www.5280.com/neighborhoods/'
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

def remove_tags(s): 
    tag = re.compile('<.*?>')
    return re.sub(tag, '', s)

# TODO: finish the scraper
if __name__ == "__main__":


    #Begin HTML Scrape: 
    