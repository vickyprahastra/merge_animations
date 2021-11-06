from PIL import Image, ImageSequence
from os import walk
import os
import json
import time

images_dir = 'images'
metadata_dir = 'metadata'
animations_dir = 'animations'
final_dir = 'final'
tmp_dir = 'sequence'
animation_frames = 30
start_time = time.time()

file_range = len(os.listdir(metadata_dir)) # get files range

def check_or_create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

check_or_create_directory(tmp_dir)
check_or_create_directory(final_dir)


def image_open(frame):
    return Image.open(frame).convert('RGBA')

for index in range(file_range):
    json_file = open(f'{metadata_dir}/{index}')
    data = json.load(json_file)
    animations_list_for_object = []
    final_frames = []

    for i in data['attributes']:
        if i['trait_type'].lower() in os.listdir(f'{tmp_dir}'):
            if i['value'].lower().replace(" ", "_") in os.listdir(f'{tmp_dir}/{i["trait_type"].lower()}'):
                animations_list_for_object.append(f'{tmp_dir}/{i["trait_type"].lower()}/{i["value"].lower().replace(" ", "_")}')


    for x in range(animation_frames):
        body = image_open(f'{images_dir}/{index}.png')
        for animation_list in animations_list_for_object:

            animation_frame = image_open(f'{animation_list}/{x}.png')
            body.paste(animation_frame, mask=animation_frame)

            final_frames.append(body)

    final_frames[0].save(f'{final_dir}/{index}.gif', save_all=True, append_images=final_frames[1:], loop=0, duration=30)

    print(f'Image of {index} successfully merged in {round((time.time() - start_time), 2)} seconds')
    json_file.close()
