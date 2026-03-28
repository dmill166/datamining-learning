# Activity 05

## PDF Content Extraction using GCP's Cloud Vision API

## Goal
The goal of this activity is to illustrate how to use GCP's Cloud Vision API to extract information from a PDF document. 
 
## Steps

### Step 1 - Setup a GCP Project

Follow the steps described under Resources - GCP 101 to create a new project named "cv-pdf". Make sure to enable the Cloud Vision API on this project. This time you will need to create a service account (instead of an API KEY). 

* Choose Credentials
* Manage service accounts
* Create Service Account
    * Name: cv-pdf-account
    * Role: owner
* Create private key for the service account (type json)

Copy the json file to a protected folder (for example, files under this activity main folder). Then set the GOOGLE_APPLICATION_CREDENTIALS environment variable with the path to the credentials file. 

```
export GOOGLE_APPLICATION_CREDENTIALS=../files/cv-pdf-323419-a6ddc5a33453.json
```

### Step 2 - Create a GCP Bucket

GCP's Cloud Vision API requires that converted pdf files to be stored in a GCP's storage bucket. Select "Cloud Storage" in your GCP web console and then browser. If this is the first time you are using this service you need to enable billing. After that, create a bucket with an unique name, e.g. "interminent-drips". Choose "Region" for the location type for your bucket and "Standard" for the storage class. 

### Step 3 - Write the Code

Complete the TO-DO's in the code found in src. 

### Step 4 - Test

Begin testing the Purchase Order pdf file found under data.  Try other PDF files if you want to.  
