#####
#
#   PhotoSort
#   Author: eppixdev
#   Inspired by Feng Lu's photo organizer - http://fenglu.me/2017/06/07/Using-python-to-organize-pictures/
#
#####

import hashlib
import exifread
import datetime
import os
import shutil

FILE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.JPG', '.PNG', '.JPEG')

source_path = "C:\\Users\\Chris\\PycharmProjects\\PhotoSort\\PhotoSort\\test\\"
destination_path = "C:\\Users\\Chris\\PycharmProjects\\PhotoSort\\PhotoSort\\sorted\\"


def hash_file(filename):

    # Make a hash object
    h = hashlib.sha1()

    # Open file for reading
    with open(filename, 'rb') as file:

        # Loop until the end of the file
        chunk = 0
        while chunk != b'':
            # Read only 1024 bytes at a time
            chunk = file.read(1024)
            h.update(chunk)

    # Return the hex representation of digest
    return h.hexdigest()


def check_extension(filename):
    oldext = os.path.splitext(filename)[1]

    if oldext not in FILE_EXTENSIONS:
        pass
    return oldext


def get_image_tag(filename):

    # Read the file
    open_file = open(filename, 'rb')

    # Return the EXIF tags with exifread module
    try:
        image_tags = exifread.process_file(open_file, stop_tag='Image DateTime')

        date_taken = image_tags['EXIF DateTimeOriginal']

        converted_date = datetime.datetime.strptime(date_taken.values, '%Y:%m:%d %H:%M:%S')

        # Assign dates
        year = str(converted_date.year)
        month = str(converted_date.month).zfill(2)
        day = str(converted_date.day).zfill(2)

        # Assign times
        hour = str(converted_date.hour).zfill(2)
        minutes = str(converted_date.minute).zfill(2)
        seconds = str(converted_date.second).zfill(2)

        # Rename file and assign original extension type
        extension = check_extension(filename)
        output_file = [year, month, day, year + "-" + month + "-" + day + "__" + hour + "." + minutes + "."
                       + seconds + extension]
        return output_file

    except KeyError:
        pass
    except ValueError:
        pass


def create_dir(filename):

    date_info = get_image_tag(filename)
    try:
        out_file_path = destination_path + date_info[0] + os.sep + date_info[1]

        # Check if directory already exists, if not, make one
        if not os.path.exists(out_file_path):
            os.makedirs(out_file_path)
            print("Created directory ", out_file_path)
    except:
        pass

    return out_file_path


def rename_file(filename):

    # For copies if file name already exists
    count = 0

    date_info = get_image_tag(filename)
    try:
        renamed_file = date_info[3]
        os.rename(filename, source_path + renamed_file)

    except FileExistsError:
        count += 1
        os.rename(filename, 'Copy(' + str(count) + ') - ' + renamed_file)

    return renamed_file


def main():

    for file in os.listdir(source_path):
        if file.endswith(FILE_EXTENSIONS):
            filename = source_path + os.sep + file
            dateinfo = get_image_tag(filename)
            count = 0
            try:
                out_filepath = destination_path + os.sep + dateinfo[0] + os.sep + dateinfo[1]
                out_filename = out_filepath + os.sep + dateinfo[3]

                # Check if destination path is existing create if not
                if not os.path.exists(out_filepath):
                    os.makedirs(out_filepath)

                # Copy the picture to the organised structure
                shutil.copy2(filename, out_filename)

                # Verify if file is the same and display output
                if hash_file(filename) == hash_file(out_filename):

                    print('File copied with success to ' + out_filename)
                    os.remove(filename)

                else:
                    print('File failed to copy' + filename)

            except:
                print('File has no exif data skipped ' + filename)


main()

