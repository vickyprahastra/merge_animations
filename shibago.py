from PIL import Image, ImageSequence
from os import walk
import os
import json
import time

images_dir = 'images'
metadata_dir = 'metadata'
animations_dir = 'animations'
final_dir = 'final'
tmp_dir = 'tmp'
# animation_frames = 30
start_time = time.time()

file_range = len(os.listdir(metadata_dir)) # get files range

animations_dir_list = []
def split_all_animations():
    for (dirpath, dirnames, filenames) in walk(animations_dir):
        animations_dir_list.extend(dirnames)
        break

split_all_animations()

def check_or_create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

check_or_create_directory(tmp_dir)
check_or_create_directory(final_dir)


for anim_dir in animations_dir_list:
    for (dirpath, dirnames, filenames) in walk(f'{animations_dir}/{anim_dir}'):
        for filename in filenames:
            # print(f'{animations_dir}/{anim_dir}/{filename}')

            filename_noextension = os.path.splitext(filename)[0].replace(" ", "_")
            file_gif = Image.open(f'{animations_dir}/{anim_dir}/{filename}')

            check_or_create_directory(f'{tmp_dir}/{anim_dir}/{filename_noextension}')

            frames = []
            for frame in ImageSequence.Iterator(file_gif):
                frame = frame.copy()
                frame.save(f'{tmp_dir}/{anim_dir}/{filename_noextension}/{len(frames)}.png')
                frames.append(frame)

def image_open(frame):
    return Image.open(frame).convert('RGBA')

class ItemData():
    def __init__(self, trait_name, tmp_directory):
        self.trait_name = trait_name
        self.tmp_directory = tmp_directory

for index in range(file_range):
    json_file = open(f'{metadata_dir}/{index}')
    data = json.load(json_file)
    animations_list_for_object = []
    final_frames = []

    for i in data['attributes']:
        if i['trait_type'].lower() in os.listdir(f'{tmp_dir}'):
            if i['value'].lower().replace(" ", "_") in os.listdir(f'{tmp_dir}/{i["trait_type"].lower()}'):
                trait_tmp_directory = f'{tmp_dir}/{i["trait_type"].lower()}/{i["value"].lower().replace(" ", "_")}'
                # animations_list_for_object.append(f'{tmp_dir}/{i["trait_type"].lower()}/{i["value"].lower().replace(" ", "_")}')
                animations_list_for_object.append( ItemData(i["trait_type"], trait_tmp_directory ) )

    # print(animations_list_for_object)
    # for obj in animations_list_for_object:
        # print(obj.trait_name)






    first_animation_frame_range = len(os.listdir(animations_list_for_object[0].tmp_directory))


    for x in range(first_animation_frame_range):
        body = image_open(f'{images_dir}/{index}.png')
        if x == 0:
            not_main_frame_index = 1
        if ((x+1) % 3) == 0:
            not_main_frame_index = 0

        for i, trait in enumerate(animations_list_for_object, start=0):


            if trait.trait_name == "Background":
                animation_frame = image_open(f'{trait.tmp_directory}/{x}.png')
            else:
                animation_frame = image_open(f'{trait.tmp_directory}/{not_main_frame_index}.png')

            body.paste(animation_frame, mask=animation_frame)
            # animation_frame.paste(body, mask=body)
            final_frames.append(body)

        not_main_frame_index += 1

    final_frames[0].save(f'{final_dir}/{index}.gif', save_all=True, append_images=final_frames[1:], loop=0, duration=20)

    print(f'Image of {index} successfully merged in {round((time.time() - start_time), 2)} seconds')
    json_file.close()


