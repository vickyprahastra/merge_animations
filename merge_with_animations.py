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
animation_frames = 30
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


for index in range(file_range):
    json_file = open(f'{metadata_dir}/{index}')
    data = json.load(json_file)
    animations_list_for_object = []
    final_frames = []

    for i in data['attributes']:
        if i['trait_type'].lower() in os.listdir(f'{tmp_dir}'):
            # print(i['trait_type'].lower())
            if i['value'].lower().replace(" ", "_") in os.listdir(f'{tmp_dir}/{i["trait_type"].lower()}'):
                # print(f'{tmp_dir}/{i['trait_type'].lower()}/{i['value'].lower()}')
                animations_list_for_object.append(f'{tmp_dir}/{i["trait_type"].lower()}/{i["value"].lower().replace(" ", "_")}')


    for x in range(animation_frames):
        body = image_open(f'{images_dir}/{index}.png')
        for animation_list in animations_list_for_object:
            # print(f'{animation_list}/{x}.png')

            # mata = Image.open(f'images/mata/{x}.png').convert('RGBA')
            # tail = Image.open(f'images/tail/{x}.png').convert('RGBA')

            animation_frame = image_open(f'{animation_list}/{x}.png')
            body.paste(animation_frame, mask=animation_frame)

            # body.paste(tail, mask=tail)

            final_frames.append(body)

    final_frames[0].save(f'{final_dir}/{index}.gif', save_all=True, append_images=final_frames[1:], loop=0, duration=30)

    # print(index, animations_list_for_object)
    print(f'Image of {index} successfully merged in {round((time.time() - start_time), 2)} miliseconds')
    json_file.close()








# transparent_foreground = Image.open('body2.png')
# mata_animated_gif = Image.open('mata.gif')
# tail_animated_gif = Image.open('tail.gif')
#
# mata_frames = []
# tail_frames = []
# final_frames = []
#
# for frame in ImageSequence.Iterator(mata_animated_gif):
#     frame = frame.copy()
#     frame.save(f'images/mata/{len(mata_frames)}.png')
#     mata_frames.append(frame)
#
# for frame in ImageSequence.Iterator(tail_animated_gif):
#     frame = frame.copy()
#     frame.save(f'images/tail/{len(tail_frames)}.png')
#     tail_frames.append(frame)
#
# for x in range(30):
#     print(x)
#     mata = Image.open(f'images/mata/{x}.png').convert('RGBA')
#     tail = Image.open(f'images/tail/{x}.png').convert('RGBA')
#     body = Image.open('body2.png').convert('RGBA')
#     body.paste(mata, mask=mata)
#     body.paste(tail, mask=tail)
#     final_frames.append(body)
#
# dir_images_mata = 'images/mata'
# dir_images_tail = 'images/tail'
#
# for f in os.listdir(dir_images_mata):
#     os.remove(os.path.join(dir_images_mata, f))
#
# for f in os.listdir(dir_images_tail):
#     os.remove(os.path.join(dir_images_tail, f))
#
# # mata_frames[0].save('output.gif', save_all=True, append_images=mata_frames[1:])
# final_frames[0].save('final_output.gif', save_all=True, append_images=final_frames[1:], loop=0, duration=30)
