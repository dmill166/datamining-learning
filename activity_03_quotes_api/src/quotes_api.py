# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 03 - Quotes API

import requests
import json
import os

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname((__file__)))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
JSON_FILE_NAME = 'quotes.json'
JSON_FILE_PATH = os.path.join(DATA_FOLDER, JSON_FILE_NAME)
QUOTES_API_URL = 'http://quotes.rest/qod'

if __name__ == "__main__":

    # TODO: send the request to the API
    result = 

    # TODO: process the response
    if result.status_code == 200:
        raw_json = json.loads(result.content.decode('utf-8'))
        quotes = []
        
        
        # TODO: append quotes to json file
        

    else:
        print('Ops, something didn\'t work!')
        print(result.content)




