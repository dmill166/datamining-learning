# imports
from bs4 import BeautifulSoup
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import requests
from sklearn.metrics import r2_score
import statistics as stats
import sys
import wordninja

# Definitions/Parameters
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
#   https://msudenver.instructure.com/courses/47959/pages/cs-390z-matplotlib
#   https://stackoverflow.com/questions/6473679/transpose-list-of-lists
#   https://stackabuse.com/rotate-axis-labels-in-matplotlib/
#   https://www.educative.io/edpresso/how-to-emulate-a-do-while-loop-in-python
#   https://stackoverflow.com/questions/26785354/normalizing-a-list-of-numbers-in-python
#   https://www.geeksforgeeks.org/creating-pandas-dataframe-using-list-of-lists/


# Read in Crime Data
if __name__ == "__main__":
    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(BASE_URL, verify=False).text

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
    for x in range(len(bin_list) - 1):
        # bin_label_list.append(str(bin_list[x] / 1000) + 'K-' + str(bin_list[x + 1] / 1000) + 'K')
        bin_label_list.append(str(bin_list[x] / 1000) + 'K')

    fig, ax = plt.subplots()
    counts, bins, _ = plt.hist(
        crime_state_total,
        range=(min_x_val_histogram, max_x_value_histogram),
        bins=bin_list,
        rwidth=0.8

    )
    plt.xticks(np.arange(min_x_val_histogram, max_x_value_histogram, BIN_SIZE))
    # ax.set_xticklabels(bin_label_list, rotation='horizontal')

    plt.xlabel('Total Murders')
    plt.ylabel('Number of States')
    plt.title('Murders by state as reported by the FBI (' + str(BASE_YEAR) + ')')

    plt.show()
    print()

    crime_data_transpose = list(map(list, zip(*crime_data)))
    # for weapon_rows in crime_data_transpose:
    #     weapon_rows_length = len(weapon_rows)
    #     outliers = weapon_rows_length // 10
    #     for iterations in range(outliers):
    #         weapon_rows.remove(min(weapon_rows))
    #         weapon_rows.remove(max(weapon_rows))

    BOX_PLOTS_TO_SHOW = 3
    while len(crime_data_transpose) != BOX_PLOTS_TO_SHOW:
        for decrease_iter in range(10, 1, -1):
            threshold = max(max(crime_data_transpose)) // decrease_iter
            for sanity_check in crime_data_transpose:
                if max(sanity_check) < threshold:
                    crime_data_transpose.remove(sanity_check)
            if len(crime_data_transpose) == BOX_PLOTS_TO_SHOW:
                break

    branches = crime_data_transpose
    medians = [stats.median(branch) for branch in branches]
    plt.boxplot(
        branches
    )
    branch_labels = []
    i = 0
    for branch in branches:
        max_value = max(branch)
        plt.annotate(str(max_value), xy=(i + 1, max_value))
        plt.annotate(str(medians[i]), xy=(i + 1, medians[i]))
        branch_labels.append(crime_col_headers[i + 3])
        i += 1
    axes = plt.gca()
    axes.spines['right'].set_visible(False)
    axes.spines['top'].set_visible(False)
    axes.set_xticklabels(branch_labels)
    plt.xlabel('Murder Weapons')
    plt.ylabel('Total Murders')
    plt.title('Top 3 Murder Weapons by State as Reported by the FBI (' + str(BASE_YEAR) + ')')
    plt.show()
    print()

    census_totals_norm = [float(i) / sum(census_data_BASE_YEAR) for i in census_data_BASE_YEAR]
    crime_totals_norm = [float(i) / sum(crime_state_total) for i in crime_state_total]
    total_crime_and_census = [crime_totals_norm, census_totals_norm]

    SCATTER_NUM_OF_X_TICKS = 10
    max_x_value_x_100 = int(max(total_crime_and_census[0]) * 1000)
    scatter_x_ticks = [x for x in range(0, max_x_value_x_100, int(max_x_value_x_100 / SCATTER_NUM_OF_X_TICKS))]
    for y in range(len(scatter_x_ticks)):
        scatter_x_ticks[y] = float(scatter_x_ticks[y]) / 1000.0

    PERCENT_DATA_POINTS_SCRUBBED = 2
    num_scrub_points = math.ceil(len(crime_row_headers) * (PERCENT_DATA_POINTS_SCRUBBED / 100))

    for k in range(num_scrub_points):
        max_crime_data_point_index = crime_totals_norm.index(max(crime_totals_norm))
        crime_totals_norm.pop(max_crime_data_point_index)
        census_totals_norm.pop(max_crime_data_point_index)

        max_census_data_point_index = census_totals_norm.index(max(census_totals_norm))
        crime_totals_norm.pop(max_census_data_point_index)
        census_totals_norm.pop(max_census_data_point_index)

        min_crime_data_point_index = crime_totals_norm.index(min(crime_totals_norm))
        crime_totals_norm.pop(min_crime_data_point_index)
        census_totals_norm.pop(min_crime_data_point_index)

        min_census_data_point_index = census_totals_norm.index(min(census_totals_norm))
        crime_totals_norm.pop(min_census_data_point_index)
        census_totals_norm.pop(min_census_data_point_index)

    axes = plt.gca()
    plt.scatter(total_crime_and_census[0], total_crime_and_census[1])
    axes.set_xticklabels(scatter_x_ticks)
    plt.xlabel('Normalized State Populations')
    plt.ylabel('Normalized State Murders')
    plt.title('State Population & Murder Data (Per FBI & Census - ' + str(BASE_YEAR) + ')')
    print('Coefficient of determination: %.2f'
          % r2_score(total_crime_and_census[0], total_crime_and_census[1]))
    plt.show()
    print()
