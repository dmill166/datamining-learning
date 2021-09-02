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
    storage_client = storage.Client() 
    bucket = storage_client.get_bucket(BUCKET_NAME)

    # TODO: upload pdf file to bucket
    pdf_blob = bucket.blob(PDF_FILE_NAME)
    file_name = os.path.join(DATA_FOLDER, PDF_FILE_NAME)
    with open(file_name, 'rb') as pdf_file:
        pdf_blob.upload_from_file(pdf_file)

    # TODO: instantiate the GCP's cloud vision API client
    cv_client = vision.ImageAnnotatorClient()
    feature = vision.Feature(
        type_ = vision.Feature.Type.DOCUMENT_TEXT_DETECTION
    )
    
    # TODO: gather information about the source file
    file_name, _ = PDF_FILE_NAME.split('.')
    txt_file_name = file_name + '.txt'
    gcs_source = vision.GcsSource(uri = get_uri(PDF_FILE_NAME))
    input_config = vision.InputConfig(
        gcs_source = gcs_source, 
        mime_type = 'application/pdf'
    )

    # TODOO: gather information about the destination file
    gcs_destination = vision.GcsDestination(uri = get_uri(txt_file_name))
    output_config = vision.OutputConfig(
        gcs_destination = gcs_destination, 
        batch_size = 10
    )

    # TODO: make the API call
    print('Converting pdf...')
    request = vision.AsyncAnnotateFileRequest(
        features = [feature], 
        input_config = input_config, 
        output_config = output_config
    )

    #TODO: monitor the status of the request 
    operation = cv_client.async_batch_annotate_files(
        requests = [request]
    )

    # TODO: wait for the opeation to complete
    operation.result(timeout = 60)
    print('done!')

    # TODO: now download the json blob file with the results of the conversion
    for blob in bucket.list_blobs():
        if blob.name.startswith(file_name) and blob.name.endswith('json'):
            result = json.loads(blob.download_as_string())        
            with open(os.path.join(DATA_FOLDER, txt_file_name), 'wt') as txt_file:
                for response in result['responses']:
                    txt_file.write(response['fullTextAnnotation']['text'])
            break

        
    
 