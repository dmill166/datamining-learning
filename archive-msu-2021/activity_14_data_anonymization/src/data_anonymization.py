# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 14: data anonymization

import os
import pandas as pd
import random
import requests
import time
# from google.colab import drive
from datetime import datetime, timedelta

# definitions/parameters
original_path = os.getcwd()
os.chdir(os.path.dirname(__file__))
os.chdir('../')
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
# DATA_FOLDER     = '/content/drive/MyDrive/Colab Datasets/human_resources'
CSV_FILE_NAME   = 'employees.csv'
CSV_FILE_PATH = os.path.join(DATA_FOLDER, CSV_FILE_NAME)
ANON_CSV_FILE_NAME = 'employees_anon.csv'
ANON_CSV_FILE_PATH = os.path.join(DATA_FOLDER, ANON_CSV_FILE_NAME)
PSEUDO_NAME_API = 'https://api.namefake.com/'

# Google drive mount
# drive.mount('/content/drive')

class IdGenerator: 

  def __init__(self, min, max, total):
    self.min = min
    self.max = max 
    self.total = total

  def __iter__(self):
    self.ids = random.sample(range(self.min, self.max + 1), self.total)
    self.current = 0
    return self

  def __next__(self):
    if self.current < len(self.ids):
      value = self.ids[self.current]
      self.current += 1 
      return value
    else:
      raise StopIteration 

def get_pseudo_name_email(gender):
  while True:
    result = requests.get(PSEUDO_NAME_API)
    if result.status_code == 200:
      data = result.json()
      if 'female' in data['pict']:
        if gender == 'M':
          continue
      else:
        if gender == 'F':
          continue
      name = data['name']
      email = data['email_u'] + '@' + data['email_d']
      return name, email
    else:
      time.sleep(1)

def shift_date_days(date, days):
  shift_days = random.randrange(days * 2 + 1) - 30
  td = timedelta(days=abs(shift_days))
  if shift_days >= 0:
    return date + td
  else:
    return date - td

def shift_salary_amount(salary, min, max):
  return salary + random.randrange(2 * (max-min) + 1) - (max-min)

# TODO; finish the data anonymization
if __name__ == "__main__":

  