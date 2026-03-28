# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 14: data anonymization

import os
import pandas as pd
import random
import requests
import time
from google.colab import drive
from datetime import datetime, timedelta

# definitions/parameters
DATA_FOLDER     = '/content/drive/MyDrive/Colab Datasets/human_resources'
CSV_FILE_NAME   = 'employees.csv'
ANON_CSV_FILE_NAME = 'employees_anon.csv'
PSEUDO_NAME_API = 'https://api.namefake.com/'

# Google drive mount
drive.mount('/content/drive')

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

  df = pd.read_csv(os.path.join(DATA_FOLDER, CSV_FILE_NAME))
  df_new = pd.DataFrame(columns=['id', 'name', 'gender', 'email', 'dob', 'doj', 'years', 'salary', 'ssn', 'city', 'state', 'zipcode'])
  random_id = iter(IdGenerator(10000, 99999, 1000))
  random_ssn = iter(IdGenerator(100000000, 999999999, 1000))
  count = 0
  for index, data in df.iterrows():
    count += 1
    # if count > 5:
    #   break
    new_row = {}
    new_row['id'] = next(random_id)
    new_row['gender'] = data['Gender']
    new_row['name'], new_row['email'] = get_pseudo_name_email(new_row['gender'])
    try:
        dob = datetime.strptime(data['Date of Birth'], '%m/%d/%Y')
        new_row['dob'] = shift_date_days(dob, 30)
    except ValueError:
      pass 
    try:
      doj = datetime.strptime(data['DOW of Joining'], '%m/%d/%Y')
      new_row['doj'] = shift_date_days(doj, 30)
    except ValueError:
      pass 
    new_row['years'] = data['Age in Company (Years)']
    #print(data['Salary'])
    new_row['salary'] = shift_salary_amount(float(data['Salary']), 1000, 2500)
    ssn = str(next(random_ssn))
    new_row['ssn'] = ssn[:3] + '-' + ssn[3:5] + '-' + ssn[5:]
    new_row['city'] = data['City']
    new_row['state'] = data['State']
    new_row['zipcode'] = data['Zip']
    #print(new_row)
    df_new = df_new.append(new_row, ignore_index=True)
  
  # swapping of {city, state, zipcode}
  for swaps in range(100): # FIXME: adjust how many swappings here
    i = random.randrange(len(df_new.index))
    j = random.randrange(len(df_new.index))
    # swap of city
    city_i    = df_new.loc[i,'city']
    df_new.loc[i,'city']  = df_new.loc[j,'city']
    df_new.loc[j,'city']  = city_i
    # swap of state
    state_i    = df_new.loc[i,'state']
    df_new.loc[i,'state']  = df_new.loc[j,'state']
    df_new.loc[j,'state']  = state_i
    # swap of zipcode
    zipcode_i    = df_new.loc[i,'zipcode']
    df_new.loc[i,'zipcode']  = df_new.loc[j,'zipcode']
    df_new.loc[j,'zipcode']  = zipcode_i

  df_new.to_csv(os.path.join(DATA_FOLDER, ANON_CSV_FILE_NAME), index=False)