from os import walk
import os
import json
from pathlib import Path

metadata_dir = 'metadata'

file_range = len(os.listdir(metadata_dir)) # get files range

def check_or_create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

array = []

for index in range(file_range):
    json_file = open(f'{metadata_dir}/{index}')
    data = json.load(json_file)

    array.append(data)

data_combine = json.dumps(array, indent = 4)

print(data_combine)

with open("sample.json", "w+") as outfile:
    outfile.write(data_combine)
