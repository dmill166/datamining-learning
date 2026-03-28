# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: A Simple Web Scraper

import json 
import re 
import os
import requests
from bs4 import BeautifulSoup

# definitions/parameters
DATA_FOLDER = '../data'
JSON_FILE_NAME = 'covid_testing_denver.json'
BASE_URL = 'https://covidcheckcolorado.org/find-our-sites-testing/'
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"}

def remove_tags(s): 
    tag = re.compile('<.*?>')
    return re.sub(tag, '', s)

if __name__ == "__main__":

    # TODO: get list of covid-19 testing centers in Denver from BASE_URL, saving them in a dictionary with the structure described in README
    

    # TODO: save covid-19 testing centers in Denver to json
