# Copies n files from the subdirs where it's placed

import os
import shutil

img_extensions = ('jpg', 'jpeg', 'png')
n_imgs_to_copy = 1

# Create folder
path = os.getcwd()+"/final/"
if not os.path.exists(path):
    os.mkdir(path)


# Go one subfolder at a time and copy X images (hyperparam)
for root, dirs, files in os.walk("."):
    for count, file in enumerate(files):
        if file.endswith(img_extensions):
            if count >= n_imgs_to_copy:
                break
            shutil.copyfile(root+"/"+file, path+file)
