from PIL import Image, ImageSequence
from os import walk
import os
import json
import time
from pathlib import Path
import uuid

metadata_dir = 'metadata'
final_dir = 'final'
# rename_metadata_dir = 'rename_metadata'

file_range = len(os.listdir(metadata_dir)) # get files range

def check_or_create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# check_or_create_directory(rename_metadata_dir)

for index in range(file_range):
    json_file = open(f'{metadata_dir}/{index}.json')
    data = json.load(json_file)
    get_uuid = uuid.uuid4().hex

    filename = data['image']
    data['image'] = f'https://shibago.s3.ap-southeast-1.amazonaws.com/{index}-{get_uuid}.gif'
    print(f'https://shibago.s3.ap-southeast-1.amazonaws.com/{index}-{get_uuid}.gif')


    with open(f'{metadata_dir}/{index}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    # filepath = Path(f'{final_dir}/{index}.gif')
    # filepath.rename(filepath.with_suffix(f'{index}-{get_uuid}.gif'))
    os.rename(f'{final_dir}/{index}.gif', f'{final_dir}/{index}-{get_uuid}.gif')
