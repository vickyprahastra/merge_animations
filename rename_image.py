from PIL import Image, ImageSequence
from os import walk
import os
import json
import time
from pathlib import Path
import uuid

metadata_dir = 'metadata'
# rename_metadata_dir = 'rename_metadata'

file_range = len(os.listdir(metadata_dir)) # get files range

def check_or_create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# check_or_create_directory(rename_metadata_dir)

for index in range(file_range):
    json_file = open(f'{metadata_dir}/{index}.json')
    data = json.load(json_file)

    filename = data['image']
    # data['image'] = os.path.splitext(filename)[0]+f'-{uuid.uuid4().hex}.gif'
    print(os.path.splitext(filename)[0]+f'-{uuid.uuid4().hex}.gif')


    # with open(f'{metadata_dir}/{index}', 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)
    #
    # filepath = Path(f'{metadata_dir}/{index}')
    # filepath.rename(filepath.with_suffix('.json'))
    # print(filepath)

