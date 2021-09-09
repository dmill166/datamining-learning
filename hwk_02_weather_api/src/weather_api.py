# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Homework 02 - Weather API

import requests
import json
import os
from urllib.parse import urlencode
from datetime import datetime
import time
import math
from dotenv import load_dotenv
load_dotenv()

# Resources:
#   Investigated ways to create environment variables. Could not solve w/time constraint,
#       so came up with own solution using custom get_creds(x) method.
#   https://www.geeksforgeeks.org/python-os-getenv-method/
#   https://www.nylas.com/blog/making-use-of-environment-variables-in-python/
#   https://stackoverflow.com/questions/55647358/how-do-i-solve-error-dotenv-installation-error-on-pycharm
#   https://stackoverflow.com/questions/54488095/python-3-dictionary-key-to-a-string-and-value-to-another-string
#
#   Read over API documentation for OpenWeather to understand appropriate calls
#   https://openweathermap.org/current#bulk
#
#   Read about how to use OpenWeather API
#   https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
#
#   Read about sample case of using OpenWeather API in Python
#   https://www.geeksforgeeks.org/python-find-current-weather-of-any-city-using-openweathermap-api/
#   but didn't understand why it worked, so read documentation:
#   https://2.python-requests.org/en/master/


# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname((__file__)))
SRC_PATH = os.getcwd()
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
LOCATIONS_FILE_NAME = 'locations.csv'
LOCATIONS_PATH = os.path.join(DATA_FOLDER, LOCATIONS_FILE_NAME)
JSON_FILE_NAME = 'weather.json'
JSON_FILE_PATH = os.path.join(DATA_FOLDER, JSON_FILE_NAME)
CREDS_FILE = 'creds.rtf'
CREDS_PATH = os.path.join(SRC_PATH, CREDS_FILE)
OPEN_WEATHER_API = 'http://api.openweathermap.org/data/2.5/weather'
SLEEP_TIME = 5


def kelvin_fahrenheit(k):
    """Converts Kelvin input temperature to Celsius."""
    return math.floor((k - 273.15) * 9 / 5 + 32)


def get_creds(x):
    """Quickly constructed method to allow a local configuration file to be used and customized."""
    with open(CREDS_PATH, 'rt') as key_file:
        line_list = []
        for line in key_file:
            entry = {}
            the_line = line.split('=')
            entry[the_line[0]] = [the_line[1]]
            line_list.append(entry)
    if x == 0:
        key, value = list(line_list[0].items())[0]  # api key
        return value[0]
    # Build additional if-else to extract based on int parameter
    else:
        return 'No creds found!'


if __name__ == "__main__":
    # Gather API Key to be used
    api_key = get_creds(0)  # parameter 0 for api key
    print("Your API key is", api_key)
    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")

    # Gather locations to be used
    with open(LOCATIONS_PATH, 'rt') as csv_file:
        location_list = []
        for line in csv_file:
            location_list.append(line.strip() + ',US')

    # Perform API Call and store results
    weather_json_list = []
    for location in location_list:
        city_details = location.split(',')
        city = city_details[0]
        state = city_details[1]
        country = city_details[2]
        api_string = f'http://api.openweathermap.org/data/2.5/weather?appid={api_key}&q={city},{state},{country}&units=imperial'
        x = requests.get(api_string).json()

        if x["cod"] != "404":
            city_dict = {}
            city_dict['today'] = today
            city_dict['city'] = x['name']
            city_dict['state'] = state
            y = x["main"]
            city_dict['temp_min'] = y["temp_min"]
            city_dict['temp_max'] = y["temp_max"]
            city_dict['temp'] = y["temp"]
        weather_json_list.append(city_dict)

    print(weather_json_list)
    # Output results to JSON
    with open(JSON_FILE_PATH, 'w') as json_file:
        json_file.write(json.dumps(weather_json_list))  
        
    print('End of code!')
