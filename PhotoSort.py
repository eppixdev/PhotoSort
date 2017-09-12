#####
#
#   Photo Sort
#   Author: eppixdev
#
#####

import exifread
import os
import re

source_folder = "C:\\Users\\Chris\\PycharmProjects\\PhotoSort\\test"

file_extensions = ['.jpg',
                   '.png',
                   '.JPG',
                   '.PNG',
                   '.jpeg',
                   '.JPEG']


def walk_path(root):
    # Walk the path in source_folder
    for folders, subfolders, filenames in os.walk(source_folder):

        for file in filenames:
            get_image_tag(file)
            edit_timestamp(file)
            split_ext(file)
            rename(file)


def split_ext(file):
    # Separates extension type so it can be added back on during renaming
    oldext = os.path.splitext(file)[1]

    if oldext not in file_extensions:
        pass
    return oldext


def get_image_tag(file):
    current_file = open('test\\' + file, 'rb')
    tag = exifread.process_file(current_file)
    shoot_time_tag = 'EXIF DateTimeOriginal'
    if shoot_time_tag in tag:
        shoot_time = str(tag[shoot_time_tag])
    elif shoot_time_tag not in tag:
        shoot_time = '00:00:00 00:00:00'
    else:
        shoot_time = '00:00:00 00:00:00'
    return shoot_time


def edit_timestamp(file):

    date = re.sub(':', ' ', get_image_tag(file)).split()
    year = date[0]
    month = date[1]
    day = date[2]
    hour = date[3]
    minute = date[4]
    second = date[5]
    time = hour + "-" + minute + "-" + second
    exten = split_ext(file)

    return year + "-" + month + "-" + day + "_" + time + exten


def rename(file):
        try:
            os.rename('test\\' + file, 'test\\' + edit_timestamp(file))
        except FileExistsError:
            pass


walk_path(source_folder)


# TODO: Create directories based on date of photo taken, if no EXIF data available, place in MISC
# TODO: Check image hash for duplicates
