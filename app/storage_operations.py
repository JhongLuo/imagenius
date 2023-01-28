import os

allowed_ext = {'jpg', 'jpeg', 'png', 'gif'}
file_counter = 0
images_folder = './app/images'

# clear all images in the folder
def clear_images():
    file_counter = 0
    # delete all files in ./images
    for filename in os.listdir(images_folder):
        os.remove(images_folder + filename)

def allowed_file(filename):
    return '.' in filename and filename.split('.')[-1] in allowed_ext

# generate a new filename for the image
def get_new_filename(filename):
    if allowed_file(filename):
        global file_counter
        # get the extension of the filename
        ext = filename.split('.')[-1]
        # generate a new filename
        new_filename = str(file_counter) + '.' + ext
        file_counter += 1
        return new_filename   
    else:
        raise Exception('File extension not allowed')

# store the image in the folder
def store_image(file):
    # get the new filename
    new_filename = get_new_filename(file.filename)
    # save the image in the folder
    file.save(images_folder + new_filename)
    return new_filename 