import os
import shutil
from os.path import join

SRC = "/data/alberto/datasets/ImageNet/ILSVRC2017/ILSVRC/Data/CLS-LOC/train"
root_folder = "train/"

if not os.path.isdir(root_folder):
    os.mkdir(root_folder)

n = 500
for root, dirs, files in os.walk(SRC, topdown=False):
    dst_folder = root.split("/")[-1]
    new_folder = join(os.getcwd(), root_folder, dst_folder)
    if not os.path.isdir(new_folder):
        os.mkdir(new_folder)
        print("[+] Created {}".format(new_folder))

    # Move the files to the correspondent dir
    for i, fname in enumerate(files):
        src = join(root, fname)
        dst = join(os.getcwd(), root_folder, dst_folder, fname)

        shutil.copyfile(src, dst)

        if i == n-1:
            print("[+]: Done copying for {}".format(dst_folder))
            break

