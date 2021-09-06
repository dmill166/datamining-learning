# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Student: Dakota M. Miller
# Description: Homework 01 - XLSX Data Load

#Resources:
#   Beautiful Soup Documentation:
#       https://www.crummy.com/software/BeautifulSoup/bs4/doc/#
#
#   Unzipping an xlsx file:
#       https://apple.stackexchange.com/questions/175076/how-to-open-a-zip-file-which-is-embedded-in-xlsx-file/175078
#   
#   Used for viewing XML in semi-readable format:
#       https://codebeautify.org/xmlviewer
#
#   Read about JSON library to understand implementation
#       https://docs.python.org/3/library/json.html
#
#   Looked up sample JSON to understand desired output
#       https://cloud.google.com/bigquery/images/create-schema-array.png
#
#   Reviewed Python file I/O
#       https://docs.python.org/3/library/functions.html#open
#
#   Looked up sample use of dumps() method to ensure I was using it correctly
#       https://pythonexamples.org/python-list-to-json/#4

from bs4 import BeautifulSoup
import os
import json

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname((__file__)))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
ATHLETES_FILE_NAME = 'sheet1.xml'
ATHLETES_FILE_PATH = os.path.join(DATA_FOLDER, ATHLETES_FILE_NAME)
SS_FILE_NAME = 'sharedStrings.xml'
SS_FILE_PATH = os.path.join(DATA_FOLDER, SS_FILE_NAME)
NUMBER_OF_HEADERS = 3
JSON_FILE_NAME = 'athletes.json'
JSON_FILE_PATH = os.path.join(DATA_FOLDER, JSON_FILE_NAME)

if __name__ == "__main__":

    # TODO: creates a list with all strings found in "sharedStrings.xml"
    with open(SS_FILE_PATH) as fp:
        ss_file_soup = BeautifulSoup(fp, 'xml')
        shared_strings_results = ss_file_soup.find_all('t')
        shared_strings = []
        for result in shared_strings_results:
            shared_strings.append(result.next)

        # Build custom header list & remove headers from the shared strings list
        header_list = shared_strings[len(shared_strings) - NUMBER_OF_HEADERS:]
        shared_strings = shared_strings[:-NUMBER_OF_HEADERS]

    # TODO: read contents of "athletes.xml" into a list of dictionaries
    with open(ATHLETES_FILE_PATH) as fp:
        athlete_file_soup = BeautifulSoup(fp, 'xml')

        # First, read the cell index mappings into a list
        athlete_value_results = athlete_file_soup.find_all('v')
        athlete_cell_values = []
        for result in athlete_value_results:
            athlete_cell_values.append(result.contents[0])
        athlete_cell_values = athlete_cell_values[NUMBER_OF_HEADERS:]
    
        # Then, iterate through the mappings and use an index lookup on the shared strings list to build dictionaries
        athletes_dict_list = []
        e = 0
        while e < len(athlete_cell_values):
            athlete_dict = {}
            for i in range(0, len(header_list)):
                athlete_dict[header_list[i]] = shared_strings[int(athlete_cell_values[e])]
                e += 1
            athletes_dict_list.append(athlete_dict)
    
    # TODO: write list into json file
    with open(JSON_FILE_PATH, 'w') as json_file:
        json_file.write(json.dumps(athletes_dict_list))   
    
    # Restore path back to original (in case other functions should follow that need original working directory)
    os.chdir(original_path)