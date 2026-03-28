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
    db_user   = os.getenv('DB_USER')
    db_passwd = os.getenv('DB_PASSWD')

    try:
        # TODO: connect to db
        db = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=db_user,
            password=db_passwd,
            autocommit=True
        )
        print('DB connection successful!')

        # TODO: check if csv file exists
        file_name = os.path.join(DATA_FOLDER, CSV_FILE_NAME)
        if not (os.path.isfile(file_name)):
            print('Couldn\'t find ' + file_name)
            sys.exit(1)

        # TODO: process csv file
        cursor = db.cursor()
        sql = 'INSERT INTO Employees VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        count = 0
        with open(os.path.join(DATA_FOLDER, CSV_FILE_NAME), 'rt') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                try:
                    cursor.execute(sql, row)
                    count += 1
                except:
                    print('Error: insert failed!')
            print(count, 'record(s) inserted.')

        # TODO: close db connection
        db.close()

        print('Done!')
        
    except Exception as err: 
        print(err)
