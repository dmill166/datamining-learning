# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: GCP Cloud Vision API Example

import json 
import re 
import os
from google.cloud import vision
from google.cloud import storage

# definitions/parameters
DATA_FOLDER = '../data'
PDF_FILE_NAME = 'Purchase Order.pdf'
JSON_FILE_NAME_SUFFIX = '.txtoutput-1-to-1.json'
BUCKET_NAME = 'interminent-drips'

def get_uri(file_name):
    return 'gs://' + BUCKET_NAME + '/' + file_name

# requirements: API_KEY environment variable
if __name__ == "__main__":

    # TODO: instantiate a GCP's storage API client and get a reference to bucket
    

    # TODO: upload pdf file to bucket
    

    # TODO: instantiate the GCP's cloud vision API client
    
    
    # TODO: gather information about the source file
    

    # TODOO: gather information about the destination file
    

    # TODO: make the API call
    

    #TODO: monitor the status of the request 
    

    # TODO: wait for the opeation to complete
    

    # TODO: now download the json blob file with the results of the conversion
    