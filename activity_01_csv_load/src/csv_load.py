# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 01 - CSV Data Load

import mysql.connector 
import csv
import os
import sys

# definitions/parameters
DATA_FOLDER = '../data'
CSV_FILE_NAME = 'employees.csv'
DB_HOST = 'localhost'
DB_NAME = 'hr'

if __name__ == "__main__":

    # TODO: get db connection parameters
    db_user   = 
    db_passwd = 

    try:
        # TODO: connect to db
        db = mysql.connector.connect(
            host=,
            database=,
            user=,
            password=
        )
        print('DB connection successful!')

        # TODO: check if csv file exists
        

        # TODO: process csv file
        cursor = db.cursor()
        sql = 'INSERT INTO Employees VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        count = 0
        with open(os.path.join(DATA_FOLDER, CSV_FILE_NAME), 'rt') as csv_file:
            
            print(count, 'record(s) inserted.')

        # TODO: close db connection
        

        print('Done!')
        
    except Exception as err: 
        print(err)
