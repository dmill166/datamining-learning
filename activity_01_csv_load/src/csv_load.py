# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 01 - CSV Data Load

# Contributions:
#   The following web pages helped me come up with the solution
#       of gathering the file path & tweaking to find the data folder/file:
#   https://note.nkmk.me/en/python-os-getcwd-chdir/
#   https://www.bogotobogo.com/python/python_files.php
#   https://note.nkmk.me/en/python-script-file-path/
#
#   Reviewed multiple pages from documentation for MySQL Connector:
#   https://dev.mysql.com/doc/connector-python/en/connector-python-introduction.html
#
#   Reviewed multiple pages from documentation for reading/writing files:
#   https://docs.python.org/3/tutorial/inputoutput.html#tut-files
#
#   Utilized the dictionary format for using a cursor to insert records:
#   https://dev.mysql.com/doc/connector-python/en/connector-python-example-cursor-transaction.html
#
#   Researched to resolve mysql.connector issue (two versions installed, 
#       needed only mysql-connector-python, NOT mysql-connector):
#   https://stackoverflow.com/questions/50557234/authentication-plugin-caching-sha2-password-is-not-supported

import mysql.connector 
import os
import sys
from mysql.connector import errorcode


# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname((__file__)))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME = 'employees.csv'
DB_HOST = 'localhost'
DB_NAME = 'hr'

if __name__ == "__main__":

    # TODO: get db connection parameters
    db_user   = 'hr_admin'
    db_passwd = '135791'

    try:
        # TODO: connect to db
        db = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=db_user,
            password=db_passwd
        )
        print('DB connection successful!')

        # TODO: check if csv file exists
        if not os.path.isfile(os.path.join(DATA_FOLDER, CSV_FILE_NAME)):
            print("Sorry, that doesn't exist!")
            sys.exit(1)
        print("Success! Found the file!")
        

        # TODO: process csv file
        cursor = db.cursor()
        sql = 'INSERT INTO Employees VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
        count = 0
        with open(os.path.join(DATA_FOLDER, CSV_FILE_NAME), 'rt') as csv_file:
            for line in csv_file:
                line_list = ((csv_file.readline().strip().split(',')))
                cursor.execute(sql, line_list)
                count += 1   
                db.commit() 
            print(count, 'record(s) inserted.')

        # TODO: close db connection
        db.close()
        
        # Restore path back to original (in case other functions should follow that need original working directory)
        os.chdir(original_path)
        print('Done!')
        
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
