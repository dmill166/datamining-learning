# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: A Simple Web Scraper

import json
import re
import os
import requests
from bs4 import BeautifulSoup

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME = 'covid_testing_denver.json'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, JSON_FILE_NAME)
BASE_URL = 'https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-20'
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/81.0.4044.141 Safari/537.36"}


def remove_tags(s):
    tag = re.compile('<.*?>')
    return re.sub(tag, '', s)


if __name__ == "__main__":

    # TODO: get list of covid-19 testing centers in Denver from BASE_URL, saving them in a dictionary with the
    #  structure described in README
    content = requests.get(BASE_URL, headers=HEADERS).content
    soup = BeautifulSoup(content, 'html.parser')
    divs = soup.find_all('div', {'class': 'panel panel-default wpb_accordion_section group'})
    for div in divs:
        title = div.find('span').contents[0]
        if title == 'Denver Metro Region':
            detail = div.find_all('div', {'class': 'uncode_text_column'})[0]
            paragraphs = detail.find_all('p')
            centers = []
            for paragraph in paragraphs:
                center = {}
                count = 0
                for value in paragraph.contents:
                    value = str(value)
                    value = remove_tags(value)
                    value = re.sub(r'[\n\xa0]', '', value)
                    count += 1
                    if count == 1:
                        center['name'] = value
                        if '(offers saliva testing)' in center['name']:
                            center['saliva_testing'] = True
                        if '(indoor testing)' in center['name']:
                            center['indoor_testing'] = True
                        center['name'] = re.sub(r'\(.+\)', '', center['name'])
                        center['name'] = re.sub(r' – .+$', '', center['name'])
                        center['name'] = center['name'].strip()
                    if len(value) == 0:
                        continue
                    match = re.search(r'(\w+), ([A-Z]{2}) ([\d-]+)', value)
                    if match:
                        center['city'] = match.group(1)
                        center['state'] = match.group(2)
                        center['zipcode'] = match.group(3)
                    else:
                        match = re.search(r'Hours of Operation: (.+)', value)
                        if match:
                            center['hours_of_operation'] = match.group(1)
                        elif 'hours_of_operation' in center:
                            center['hours_of_operation'] += value
                        else:
                            center['address'] = value
                centers.append(center)

    # TODO: save covid-19 testing centers in Denver to json
    with open(JSON_FILE_PATH, 'wt') as json_file:
        json.dump(centers, json_file)
