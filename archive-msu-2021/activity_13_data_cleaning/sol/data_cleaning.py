# CS390Z - Introduction to Data Minining - Fall 2021
# Instructor: Thyago Mota
# Description: Activity 12: data cleaning

from google.colab import drive
import csv 
import os
import matplotlib.pyplot as plt 
import re
from datetime import datetime
import sys

# definitions/parameters
DATA_FOLDER = '/content/drive/MyDrive/Colab Datasets/orders_dataset'

# Google drive mount
drive.mount('/content/drive')

def clean_up(text): 
  text = re.sub('[^\w\s\-&]', '', text)
  return re.sub(' +', ' ', text).strip()

def capitalize(text):
    s = ''
    for word in text.split(' '):
        s += word.lower().capitalize() + ' '
    return s.strip()

if __name__ == "__main__":

  # TODO: parse items
  # for category, if 'music' replace with 'musical instruments', if 'appliance' replace with 'appliances', and if 'office' replace with 'office suplies'
  # make sure all descriptions, units, and categories are lower case/capitalized and only contain alphanumerical, the dash, and the ampersand characters
  items = {}
  with open(os.path.join(DATA_FOLDER, 'items.csv'), 'rt') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
      code = row['code']
      descr = row['description']
      descr = clean_up(descr)
      descr = capitalize(descr)
      unit  = row['unit']
      unit = clean_up(unit)
      unit = capitalize(unit)
      price = float(row['price'])
      category  = row['category']
      category = clean_up(category)
      category = category.lower()
      if category == 'music':
        category = 'music instruments'
      elif category == 'appliance':
        category = 'appliances'
      elif category == 'office':
        category = 'office suplies'
      category = capitalize(category)

      items[code] = { 
          'description': descr, 
          'unit': unit,
          'price': price,
          'category': category
      }

  # for code in items:
  #   print(items[code])

  # TODO: parse orders
  # make sure order# uses the format 99999-XX, where XX is a 2-letter in uppercase
  # if order# users the format 99999, assume XX = CO
  # datetime may appear in formats: %Y-%m-%d %H:%M:%S or %m/%d/%y %H:%M or %m/%d/%y %H:%M:%S
  # make sure all client names, addresses and cities are lower case/capitalized and only contain alphanumerical, the dash, and the ampersand characters
  # for state, make sure they use the format XX, where XX is a 2-letter in uppercase
  # if state is Texas, replace with TX
  # check for valid email format (when informed)
  # make sure item codes are valid (ie, item exists)
  orders = {}
  with open(os.path.join(DATA_FOLDER, 'orders.csv'), 'rt') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
      order_number = row['order#']
      match = re.search('^[0-9]{5}-[A-Z]{2}$', order_number)
      if not match:
        match = re.search('^[0-9]{5}$', order_number) 
        if match:
          order_number = order_number + '-CO'
        else:
          raise Exception('Order# ' + order_number + ' is invalid!')
      date_time = None
      try:
        date_time = datetime.strptime(row['datetime'], '%Y-%m-%d %H:%M:%S')
      except ValueError:
        pass 
      try:
        if not date_time:
          date_time = datetime.strptime(row['datetime'], '%m/%d/%y %H:%M')
      except ValueError as err:
        pass   
      try:
        if not date_time:
          date_time = datetime.strptime(row['datetime'], '%m/%d/%y %H:%M:%S')
      except ValueError as err:
        print(row['datetime'])
        raise err   
      client = clean_up(row['client'])
      client = capitalize(client)
      address = clean_up(row['address'])
      address = capitalize(address)
      city = clean_up(row['city'])
      city = capitalize(city)
      state = row['state'].upper()
      match = re.search('^[A-Z]{2}$', state)
      if not match:
        if state == 'TEXAS':
          state = 'TX'
      email = row['email']
      if len(email) > 0:
        match = re.search('^[^@]+@[^@]+\.[^@]+$', email)
        if not match:
          raise Exception('Invalid email!')
      code = row['code']
      if code not in items:
        raise Exception('Item ' + code + ' was not found!')
      qtt = int(row['qtt'])
      if order_number not in orders:
        orders[order_number] = {
              'date_time': date_time, 
              'client': client, 
              'address': address,
              'city': city, 
              'state': state,
              'email': email,
              'items': []
          }
      orders[order_number]['items'].append({
          'code': code,
          'qtt': qtt
      })

  # for order_number in orders:
  #   print(orders[order_number])
  #   print()
          
  # display a line plot showing the total orders per month per state in the year 2021 
  states = {}
  for order_number in orders:
    state = orders[order_number]['state']
    if orders[order_number]['date_time'].year != 2021:
      continue
    if state not in states:
      states[state] = [ 0 ] * 12
    month = orders[order_number]['date_time'].month
    for item in orders[order_number]['items']:
      states[state][month-1] += int(items[item['code']]['price'] * item['qtt'] * 100) / 100
  labels = []
  for state in states:
    labels.append(state)
    plt.plot(list(range(1,13)), states[state])
  plt.legend(labels)
  plt.grid()
  axes = plt.gca()
  axes.set_xticks(list(range(1,13)))
  plt.xlabel('Month')
  plt.ylabel('Sales ($)')
  plt.title('Total Sales per State')
  plt.show()