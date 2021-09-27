# imports
import json
import numpy as np
import csv
import os
import matplotlib.pyplot as plt
import re

# Definitions/Parameters
original_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
CRIME_FILE_NAME = 'crime_data.csv'
CRIME_FILE_PATH = os.path.join(DATA_FOLDER, CRIME_FILE_NAME)
CENSUS_FILE_NAME = 'census_data.csv'
CENSUS_FILE_PATH = os.path.join(DATA_FOLDER, CENSUS_FILE_NAME)
BASE_YEAR = 2019

# Resources:
# Referenced to determine identification of digits in Python strings:
#   https://www.pythonpool.com/python-check-if-string-is-integer/
# Referenced regarding encoding issue encountered on MacOS while reading CSV:
#   http://python-notes.curiousefficiency.org/en/latest/python3/text_file_processing.html#what-changed-in-python-3
# Referenced regarding removing commas from string version of numbers in Python:
#   https://www.kite.com/python/answers/how-to-remove-a-comma-from-a-string-in-python
# Referenced how to print numbers with commas

# Read in Crime Data
if __name__ == "__main__":
    crime_col_headers = []
    crime_row_headers = []
    total_crimes = []
    crime_data = []
    crime_state_total = []
    with open(CRIME_FILE_PATH, 'rt', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        row_count = 0
        for row in reader:
            state_total = 0
            index = 0
            row_data = []
            row_count += 1
            if row_count == 1:
                for item in row:
                    if item[-1].isdigit():
                        crime_col_headers.append(item[0:-1])
                    else:
                        crime_col_headers.append(item)
            else:
                for item in row:
                    if index == 0:
                        if item[-1].isdigit():
                            crime_row_headers.append(item[0:-1])
                        else:
                            crime_row_headers.append(item)
                        index += 1
                    else:
                        row_data.append(int(item.replace(',', '')))
                        state_total += int(item.replace(',', ''))
                crime_data.append(row_data[0:])
                crime_state_total.append(state_total)

    # Read in Census Data
    census_data = []
    census_col_headers = []
    census_regions = []
    census_subcategories = []
    census_states = []
    census_data_2019 = []
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
                    census_data_2019.append(census_state_data[-1])
                census_data.append(census_state_data)
    for data in census_data:
        continue
    print()

    crimes_total_array = np.array(crime_state_total)
    print('*** Summary Statistics of 2019 Crimes Data ***')
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

    census_totals_2019_array = np.array(census_data_2019)
    print('\n*** Summary Statistics of 2019 Census Data ***')
    census_records = '{:,.0f}'.format(len(census_states))
    print(f'#records: {census_records}')
    census_minimum = '{:,.0f}'.format(np.min(census_totals_2019_array))
    census_maximum = '{:,.0f}'.format(np.max(census_totals_2019_array))
    print(f'2019 Census Range: [{census_minimum} , {census_maximum}]')
    census_mean = '{:,.2f}'.format(np.mean(census_totals_2019_array))
    print(f'2019 Census Mean: {census_mean}')
    census_median = '{:,.0f}'.format(np.median(census_totals_2019_array))
    print(f'2019 Census Median: {census_median}')
    census_std = '{:,.2f}'.format(np.std(census_totals_2019_array))
    print(f'2019 Census StD: {census_std}\n\n')

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
