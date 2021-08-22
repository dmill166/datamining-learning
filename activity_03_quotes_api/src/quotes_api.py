# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 03 - Quotes API

import requests
import json
import os

# definitions/parameters
DATA_FOLDER = '../data'
JSON_FILE_NAME = 'quotes.json'
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




