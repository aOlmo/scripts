import os
import cv2 as cv
import scipy.misc
import face_recognition

from PIL import Image
from tqdm import tqdm

file_extensions = ('.jpg', 'jpeg', '.png')

resize = (64, 64)
dir_name = "cropped_resized_images/"
path = os.getcwd()+"/"+dir_name

try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)

skipped = 0
count = 0
print("Cropping, resizing and saving new images in", dir_name, "...")
for file in tqdm(os.listdir()):
    if file.lower().endswith(file_extensions):
        count += 1
        img_name = file

        # Obtain bounding box
        image = face_recognition.load_image_file(img_name)
        # Coordinates are top, right, bottom, left
        face_locations = face_recognition.face_locations(image)

        if not len(face_locations):
            skipped += 1
            continue

        face_locations = face_locations[0]

        # Obtain cropped image
        image = Image.open(img_name)
        cropped_image = image.crop(
            # left, top, right, bottom
            (face_locations[3]-8, face_locations[0]-20, face_locations[1]+8, face_locations[2])
        )

        # Resizing of the images
        cropped_image = cropped_image.resize(resize)

        # Some of the images have a 4th channel, use only 3
        cropped_image = cropped_image.convert('RGB')
        scipy.misc.imsave(os.getcwd()+"/"+dir_name+"cr_rs_"+img_name, cropped_image)

print("Skipped:", skipped, "from a total of:", count)
