import os
import random

from tqdm import tqdm
from shutil import move, copyfile

exts = ('png', 'jpg', 'jpeg')

remove_imgs = 0
num_imgs_total = 16900
n_train = 15500
n_val = num_imgs_total - n_train


all_images_pth = os.path.join(".", "P")

# For dup function
remove_from_path = "."
compare_to_path = os.path.join(".", "all")


# 1) Remove all images by names from the training set
def remove_dup_imgs_from_training_set(remove_from_path, compare_to_path):
    remove_files = os.listdir(remove_from_path)

    c = 0
    for root, dirs, files in os.walk(".", topdown=False):
        if root == compare_to_path:
            for f in files:
                if f in remove_files:
                    os.remove(os.path.join(remove_from_path, f))
                    c += 1

    print("Removed {} images".format(c))

def divide_into_train_val(n_train, n_val):
    train_pth = os.path.join(all_images_pth, "train/")
    val_pth = os.path.join(all_images_pth, "validation/")

    # os.rmdir(train_pth)
    # os.rmdir(val_pth)

    train_sample = random.sample(os.listdir(all_images_pth), k=n_train)

    if make_dirs:
        os.mkdir(train_pth)
        os.mkdir(val_pth)

    c_train = 0
    c_val = 0
    for root, dirs, files in os.walk(all_images_pth, topdown=False):
        if root == all_images_pth:
            for f in files:
                if f in train_sample:
                    if c_train < n_train:
                        move(os.path.join(root, f), os.path.join(train_pth, f))
                        c_train += 1
                else:
                    if c_val < n_val:
                        move(os.path.join(root, f), os.path.join(val_pth, f))
                        c_val += 1

    print("[+]: Moved {}/{} train/val".format(c_train, c_val))

def keep_n_imgs(num_imgs_to_keep, pth):
    all_jpgs = [x for x in os.listdir(pth) if x.endswith(exts)]
    to_keep = random.sample(all_jpgs, k=num_imgs_to_keep)

    pth_keep = "kept_folder/"
    os.mkdir(pth_keep)

    for f in to_keep:
        copyfile(os.path.join(pth, f), os.path.join(pth_keep, f))


if __name__ == '__main__':

    make_dirs = 1
    # divide_into_train_val(n_train, n_val)
    remove_dup_imgs_from_training_set(remove_from_path, compare_to_path)
    keep_n_imgs(num_imgs_total, ".")





