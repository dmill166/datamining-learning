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

# definitions/parameters
DATA_FOLDER    = os.path.join('..', 'data')
LOCATIONS_FILE_NAME = 'locations.csv'
JSON_FILE_NAME = 'weather.json'
OPEN_WEATHER_API = 'http://api.openweathermap.org/data/2.5/weather'
SLEEP_TIME = 5

def kelvin_fahrenheit(k):
    return math.floor((k - 273.15) * 9 / 5 + 32)

if __name__ == "__main__":
    api_key = os.getenv('API_KEY')
    today = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
