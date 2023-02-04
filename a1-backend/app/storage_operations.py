import os
import base64
from werkzeug.datastructures import FileStorage

global file_counter

file_counter = 0
images_folder = './app/images'

# clear all images in the folder
def clear_images():
    global file_counter
    file_counter = 0
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)
    # delete all files in ./images
    for filename in os.listdir(images_folder):
        os.remove(os.path.join(images_folder, filename))

# generate a new filename for the image
def get_new_filename():
    global file_counter
    # generate a new filename
    new_filename = str(file_counter)
    file_counter += 1
    return new_filename

# store the image in the folder
def store_image(file):
    new_filename = get_new_filename()
    with open(get_image_path(new_filename), 'wb') as f:
        f.write(file.encode('utf-8'))
    return new_filename

def read_image(filename):
    with open(get_image_path(filename), 'rb') as f:
        return f.read().decode('utf-8')

def delete_image(filename):
    os.remove(get_image_path(filename))

# get the path of the image
def get_image_path(filename):
    return os.path.join(images_folder, filename)

