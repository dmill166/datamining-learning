# imports
import csv
import os
import sys
import numpy as np
import requests
import wordninja
from bs4 import BeautifulSoup

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

# Definitions/Parameters
from matplotlib import pyplot as plt, colors
from matplotlib.pyplot import legend

original_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CENSUS_FILE_NAME = 'census_data.csv'
CENSUS_FILE_PATH = os.path.join(DATA_FOLDER, CENSUS_FILE_NAME)
BASE_YEAR = 2019
BASE_URL = 'https://ucr.fbi.gov/crime-in-the-u.s/2019/crime-in-the-u.s.-2019/topic-pages/tables/table-20'
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) "
                         "Chrome/81.0.4044.141 Safari/537.36"}

# Resources:
#   https://www.pythonpool.com/python-check-if-string-is-integer/
#   http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html#what-changed-in-python-3
#   https://www.kite.com/python/answers/how-to-remove-a-comma-from-a-string-in-python
#   https://www.pluralsight.com/guides/extracting-data-html-beautifulsoup
#   https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attributes
#   https://stackoverflow.com/questions/8870261/how-to-split-text-without-spaces-into-list-of-words
#   https://www.geeksforgeeks.org/python-string-join-method/
#   https://stackoverflow.com/questions/5193811/how-can-i-check-for-a-new-line-in-string-in-python-3-x

# Read in Crime Data
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
        crime_col_headers[compound_headers_index] = word_sep.join(
            wordninja.split(crime_col_headers[compound_headers_index]))
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
            crime_data.append(new_state_row[2:])

    # Read in Census Data
    census_data = []
    census_col_headers = []
    census_regions = []
    census_subcategories = []
    census_states = []
    census_data_BASE_YEAR = []
    with open(CENSUS_FILE_PATH, 'rt', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        row_count = 0
        for row in reader:
            index = 0
            census_state_data = []
            row_count += 1
            if row_count == 1:
                for item in row:
                    census_col_headers.append(str(item))
            else:
                for item in row:
                    if index == 0:
                        census_regions.append(item)
                    elif index == 1:
                        census_subcategories.append(item)
                    else:
                        census_state_data.append(int(item.replace(',', '')))
                    index += 1
                if census_regions[-1] == 'State':
                    census_states.append(census_subcategories[-1])
                    census_data_BASE_YEAR.append(census_state_data[-1])
                census_data.append(census_state_data)
    for data in census_data:
        continue
    print()

    crimes_total_array = np.array(crime_state_total)
    print('*** Summary Statistics of ' + str(BASE_YEAR) + ' Crimes Data ***')
    crime_records = '{:,.0f}'.format(len(crime_state_total))
    print(f'#records: {crime_records}')
    crimes_minimum = '{:,.0f}'.format(np.min(crimes_total_array))
    crimes_maximum = '{:,.0f}'.format(np.max(crimes_total_array))
    print(f'Count of Crimes Range: [{crimes_minimum} , {crimes_maximum}]')
    crimes_mean = '{:,.2f}'.format(np.mean(crimes_total_array))
    print(f'Count of Crimes Mean: {crimes_mean}')
    crimes_median = '{:,.0f}'.format(np.median(crimes_total_array))
    print(f'Count of Crimes Median: {crimes_median}')
    crimes_std = '{:,.2f}'.format(np.std(crimes_total_array))
    print(f'Count of Crimes StD: {crimes_std}')

    census_totals_BASE_YEAR_array = np.array(census_data_BASE_YEAR)
    print('\n*** Summary Statistics of ' + str(BASE_YEAR) + ' Census Data ***')
    census_records = '{:,.0f}'.format(len(census_states))
    print(f'#records: {census_records}')
    census_minimum = '{:,.0f}'.format(np.min(census_totals_BASE_YEAR_array))
    census_maximum = '{:,.0f}'.format(np.max(census_totals_BASE_YEAR_array))
    print(f'{str(BASE_YEAR)} Census Range: [{census_minimum} , {census_maximum}]')
    census_mean = '{:,.2f}'.format(np.mean(census_totals_BASE_YEAR_array))
    print(f'{str(BASE_YEAR)} Census Mean: {census_mean}')
    census_median = '{:,.0f}'.format(np.median(census_totals_BASE_YEAR_array))
    print(f'{str(BASE_YEAR)} Census Median: {census_median}')
    census_std = '{:,.2f}'.format(np.std(census_totals_BASE_YEAR_array))
    print(f'{str(BASE_YEAR)} Census StD: {census_std}\n\n')

    BIN_SIZE = 200
    min_x_val_histogram = min(crime_state_total) // BIN_SIZE
    max_x_value_histogram = ((max(crime_state_total) // BIN_SIZE) + 2) * BIN_SIZE
    bin_list = list(range(min_x_val_histogram, max_x_value_histogram, BIN_SIZE))
    bin_label_list = []
    for x in range(len(bin_list)):
        #bin_label_list.append(str(bin_list[x] / 1000) + 'K-' + str(bin_list[x + 1] / 1000) + 'K')
        bin_label_list.append(str(bin_list[x] / 1000) + 'K')


    fig, ax = plt.subplots()
    counts, bins, _ = plt.hist(
        crime_state_total,
        range=(min_x_val_histogram, max_x_value_histogram),
        bins=bin_list,
        rwidth=0.8

    )
    #plt.xticks(np.arange(min_x_val_histogram, max_x_value_histogram, BIN_SIZE))
    ax.set_xticklabels(bin_label_list, rotation='horizontal')

    plt.xlabel('Total Murders')
    plt.ylabel('Number of States')
    plt.title('Murders by state as reported by the FBI (' + str(BASE_YEAR) + ')')

    plt.show()
    print()
    """
    #%% md
    
    # Visualizations
    
    #%%
    
    # CS390Z - Introduction to Data Minining - Fall 2021
    # Instructor: Thyago Mota
    # Description: histogram
    
    from google.colab import drive
    import matplotlib.pyplot as plt
    
    # definitions/parameters
    DATA_FOLDER = '/content/drive/MyDrive/Colab Datasets/co_air_quality/'
    DATASET_NAME = 'co_air_quality.json'
    BASE_YEAR = 2020
    
    # Google drive mount
    # drive.mount('/content/drive')
    
    with open(DATA_FOLDER + DATASET_NAME, 'rt') as json_file:
        records = json.load(json_file)
    
    aqis = []
    for record in records:
        aqis.append(record['aqi'])
    
    bins = list(range(30, 185, 15))
    counts, bins, _ = plt.hist(
        aqis,
        bins=bins,
        rwidth=0.5
    )
    xticks = [x + 7 for x in bins]
    axes = plt.gca()  # get a reference to the plot's axes
    axes.set_xticks(xticks)
    plt.xlabel('AQI')
    plt.ylabel('Count')
    plt.title('Air Quality in the Denver Metro Area (2020)')
    plt.show()
    
    #%%
    
    # CS390Z - Introduction to Data Minining - Fall 2021
    # Instructor: Thyago Mota
    # Description: box plot
    
    from google.colab import drive
    import matplotlib.pyplot as plt
    
    # definitions/parameters
    DATA_FOLDER = '/content/drive/MyDrive/Colab Datasets/co_air_quality/'
    DATASET_NAME = 'co_air_quality.json'
    BASE_YEAR = 2020
    
    # Google drive mount
    # drive.mount('/content/drive')
    
    
    #%%
    
    #%%
    
    #%%
    
    #%%
    
    #%%
    
    #%%
    with open(DATA_FOLDER + DATASET_NAME, 'rt') as json_file:
        records = json.load(json_file)
    
    aqis = []
    for record in records:
        aqis.append(record['aqi'])
    
    bp = plt.boxplot(
        aqis,
        vert=False
    )
    for median in bp['medians']:
        xy = median.get_xydata()[0]
        xy[1] -= .05
        plt.annotate(str(xy[0]), xy=xy)
    
    for cap in bp['caps']:
        xy = cap.get_xydata()[0]
        xy[1] -= .05
        plt.annotate(str(xy[0]), xy=xy)
    
    min_whisker = bp['caps'][0].get_xydata()[0][0]
    max_whisker = bp['caps'][1].get_xydata()[0][0]
    
    outliers = []
    for record in records:
        if record['aqi'] < min_whisker or record['aqi'] > max_whisker:
            outliers.append(record)
    print('*** Outliers ***')
    for outlier in outliers:
        print(outlier)
    
    axes = plt.gca()
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.set_yticklabels([''])
    plt.ylabel('AQI Denver Metro Area (2020)')
    
    plt.show()
    
    #%%
    
    # CS390Z - Introduction to Data Minining - Fall 2021
    # Instructor: Thyago Mota
    # Description: time series
    
    from google.colab import drive
    import matplotlib.pyplot as plt
    from datetime import datetime, timedelta
    
    # definitions/parameters
    DATA_FOLDER = '/content/drive/MyDrive/Colab Datasets/co_air_quality/'
    DATASET_NAME = 'co_air_quality.json'
    BASE_YEAR = 2020
    
    # Google drive mount
    # drive.mount('/content/drive')
    
    with open(DATA_FOLDER + DATASET_NAME, 'rt') as json_file:
        records = json.load(json_file)
    
    aqis = [0] * 12
    counts = [0] * 12
    for record in records:
        date = datetime.strptime(record['date'], '%m/%d/%Y')
        month = date.month
        aqis[month - 1] += record['aqi']
        counts[month - 1] += 1
    
    aqis = [aqis[i] / counts[i] for i in range(12)]
    # print(aqis)
    plt.plot(list(range(1, 13)), aqis)
    axes = plt.gca()
    axes.set_xticks(list(range(1, 13)))
    plt.xlabel('Month')
    plt.ylabel('Avg. AQI')
    plt.title('AQI Denver Metro Area (2020)')
    plt.grid()
    plt.plot([1, 12], [100, 100], '+r-')
    plt.annotate('Unhealthy (for sensitive groups)', xy=[1, 101])
    plt.plot([1, 12], [50, 50], '+y-')
    plt.annotate('Moderate', xy=[1, 51])
    plt.show()
    """
