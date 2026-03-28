import os
import sys
import requests
from bs4 import BeautifulSoup
import wordninja

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
BASE_URL = 'https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-20'
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/81.0.4044.141 Safari/537.36"}


# Resources
#   https://www.pluralsight.com/guides/extracting-data-html-beautifulsoup
#   https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attributes
#   https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
#   https://www.geeksforgeeks.org/python-string-join-method/
#   https://stackoverflow.com/questions/5193811/how-can-i-check-for-a-new-line-in-string-in-python-3-x


if __name__ == "__main__":

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(BASE_URL).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "html.parser")
    table_data = soup.find('table').text.strip()
    table_header_text, table_body_text = table_data.split('\n\n\n\n\n\n\n')

    crime_col_headers = list(table_header_text.replace('\n\n\n', '\n\n').split('\n\n'))
    for compound_headers_index in range(len(crime_col_headers)):
        word_sep = ' '
        crime_col_headers[compound_headers_index] = word_sep.join(wordninja.split(crime_col_headers[compound_headers_index]))
    for header_index in range(len(crime_col_headers)):
        if crime_col_headers[header_index][-1].isdigit():
            crime_col_headers[header_index] = crime_col_headers[header_index][0:-1].title()
        else:
            crime_col_headers[header_index] = crime_col_headers[header_index].title()

    all_crime_rows = list(table_body_text.replace('\n\n\n', '\n\n').split('\n\n'))

    crime_row_headers = []
    new_state_row = []
    crime_data = []
    crime_state_total = []
    crime_state_firearm_total = []
    for element in all_crime_rows:
        if element.strip().replace(' ', '').isalnum() and not element.replace(',', '').isdigit():
            if element[-1].isdigit():
                new_state_row = [element[0:-1].strip()]
            else:
                new_state_row = [element.strip()]
        elif element.replace(',', '').isdigit():
            new_state_row.append(int(element.replace(',', '')))
        else:
            print("I don't know that data type! Abort mission!")
            sys.exit(0)

        if len(new_state_row) == 10:
            crime_row_headers.append(new_state_row[0])
            crime_state_total.append(new_state_row[1])
            crime_state_firearm_total.append(new_state_row[2])
            crime_data.append(new_state_row[3:])

    # Illustrate scrape was successful
    print(crime_col_headers)
    print(crime_row_headers)
    print(crime_state_total)
    print(crime_data)