from google.colab import drive
import os, json

# definitions/parameters
DATA_FOLDER = '/content/drive/MyDrive/Colab Datasets/smartphones'
DATASET_NAME = 'smartphones.json'

drive.mount('/content/drive')

with open(os.path.join(DATA_FOLDER, DATASET_NAME), 'rt') as json_file:
  dataset = json.load(json_file)
  new_dataset = []
  for record in dataset:
    if record['cpu'] == '?' or record['ram'] == '? GB' or record['rear_camera'] == '?' or record['front_camera'] == '?' or record['front_camera'] == 'No' or record['battery'] == '? mah':
      continue 
    if 'Hexa-Core' not in record['cpu'] and 'Octa-Core' not in record['cpu'] and 'Quad-Core' not in record['cpu'] and 'Dual-Core' not in record['cpu']: 
      continue
    new_dataset.append(record)

print('New JSON now has', len(new_dataset))

with open(os.path.join(DATA_FOLDER, DATASET_NAME), 'wt') as json_file:
  json.dump(new_dataset, json_file)
