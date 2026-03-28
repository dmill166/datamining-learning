##############################################################################
# || Purpose: Demonstrate ability to export MySQL Database to a local csv file
# || Author: Thyago Mota, Dakota M. Miller
# || Python Version In Use: 3.8.0
# || Date Created: 2021-Sep-05
# ||
# || Details: A program that exports an entire MySQL Database table to a local csv file
# ||            Adapted from https://github.com/dmill166/21FCS390Z/blob/main/activity_01_csv_load/src/csv_load.py
# ||
##############################################################################

# Utilized the following for mysqldb commands:
#   https://dev.mysql.com/doc/connectors/en/connector-python-api-mysqlcursor.html
#
# Utilized fetch all command to get table results en masse
#   https://dev.mysql.com/doc/connectors/en/connector-python-api-mysqlcursor-fetchall.html
#
# Used CSV Writer to output results into a .csv format
#   https://docs.python.org/3/library/csv.html#csv.writer
#
# Refreshed myself on Python File I/O
#   https://www.tutorialspoint.com/python/python_files_io.htm
#
# Used for solution to verify expected lines were in output file
#   https://www.kite.com/python/answers/how-to-count-the-number-of-lines-in-a-csv-file-in-python
#
# Used for solution to write rows to output file
#   https://stackoverflow.com/questions/10333343/how-to-output-a-multiple-rows-csv
#   https://docs.python.org/3/library/csv.html

import mysql.connector 
import os
import sys
import csv
from mysql.connector import errorcode


# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname((__file__)))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CSV_FILE_NAME = 'employees.csv'
DB_HOST = 'localhost'
DB_NAME = 'hr'
TABLE_NAME = 'employees'

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
        
        # TODO: Export table from MySQL Database
        cursor = db.cursor()
        sql = 'select * from ' + DB_NAME + '.' + TABLE_NAME + ';'
        cursor.execute(sql)
        rows = cursor.fetchall()
        print(len(rows), 'rows fetched.')

        # TODO: Write table to csv file
        with open(os.path.join(DATA_FOLDER, CSV_FILE_NAME), 'w') as csv_file:
            output = csv.writer(csv_file, delimiter=',')
            output.writerows(rows)
        with open(os.path.join(DATA_FOLDER, CSV_FILE_NAME), 'r') as csv_file:
            reader = csv.reader(csv_file)
            lines= len(list(reader))
        print(lines, 'record(s) written.')

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
