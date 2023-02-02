import os
import base64
from werkzeug.datastructures import FileStorage

global file_counter

allowed_ext = {'jpg', 'jpeg', 'png', 'gif'}
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

def get_ext(filename):
    return filename.split('.')[-1]

def allowed_file(filename):
    return '.' in filename and get_ext(filename)in allowed_ext

# generate a new filename for the image
def get_new_filename(filename):
    if allowed_file(filename):
        global file_counter
        # generate a new filename
        new_filename = str(file_counter) + '.' + get_ext(filename)
        file_counter += 1
        return new_filename
    else:
        raise Exception('File extension not allowed')

# store the image in the folder
def store_image(file):
    new_filename = get_new_filename(file.filename)
    file.save(get_image_path(new_filename))
    return new_filename

def delete_image(filename):
    os.remove(get_image_path(filename))

# get the path of the image
def get_image_path(filename):
    return os.path.join(images_folder, filename)

# get the image
def filename2dict(filename):
    print(filename)
    with open(get_image_path(filename), 'rb') as f:
        return {"filename": filename, "content_type": "image/" + get_ext(filename), "data": base64.b64encode(f.read()).decode()}

def fileStorage2base64(file : FileStorage):
    file_content = file.read()
    base64_content = base64.b64encode(file_content).decode()
    return base64_content

def fileStorage2dict(file : FileStorage):
    base64_content = fileStorage2base64(file)
    return {"filename": file.filename, "content_type": file.content_type, "data": base64_content}

