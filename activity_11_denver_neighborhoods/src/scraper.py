# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 11: a simple scraper

# Resources
# Researched why previous path searching was failing. Identified difference thanks to Guido
# https://mail.python.org/pipermail/python-dev/2010-February/097461.html

import csv 
import re 
import os
import requests
from bs4 import BeautifulSoup

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname((__file__)))
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

    with open(os.path.join(DATA_FOLDER, CSV_FILE_NAME), 'wt') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['name','population','home_price','schools_score','crime_rank','x_factor'])
        content = requests.get(BASE_URL, headers=HEADERS).content
        soup = BeautifulSoup(content, 'html.parser')
        trs = soup.find_all('tr')
        for tr in trs:
            row = []
            tds = tr.find_all('td')
            if len(tds) == 0:
                continue
            a = tds[0].find('a')
            row.append(a.contents[0].strip())
            pop = tds[2].contents[0]
            pop = re.sub(',', '', pop)
            row.append(int(pop))
            price = tds[3].contents[0]
            price = re.sub('[$,]', '', price)
            row.append(int(price))
            school = tds[6].contents[0]
            row.append(float(school))
            crime = tds[7].contents[0]
            row.append(int(crime))
            xfactor = tds[8].contents[0]
            row.append(float(xfactor))
            writer.writerow(row)
