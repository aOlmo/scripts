import os
import imghdr

for filename in os.listdir(os.getcwd()):
    name, ext = os.path.splitext(filename)
    
    if ext == '.png' or ext == '.jpg':
        real_ext = imghdr.what(filename)
        if ext != real_ext and ext != None and real_ext != None:
            new_filename = name + '.' + real_ext
            os.rename(filename, new_filename)

