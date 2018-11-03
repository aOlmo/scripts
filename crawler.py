import re
import os
from tqdm import tqdm

import urllib.request as urllib
from bs4 import BeautifulSoup as bs4

# Path to save the images
path = 'imgs/'
try:
    os.mkdir(path)
except OSError:
    print("Creation of the directory %s failed" % path)
else:
    print("Successfully created the directory %s " % path)

# Main URL to crawl images from
main_url = "https://cidse.engineering.asu.edu/facultyandresearch/directory/faculty/"
url_re_identifier = r"^http((?!facultyandresearch).)*(directory/).*"
image_re_identifier = r'^(alignleft).*'

html_page = urllib.urlopen(main_url)
soup = bs4(html_page, 'html.parser')

# Find where we must look for our images
links = soup.findAll("a", attrs={'href': re.compile(url_re_identifier)})
count = 0
closed_list = []
for link in tqdm(set(links)):
    count += 1

    # Get the subpages we need
    subpage = urllib.urlopen(link.get('href'))
    soup_subpage = bs4(subpage, 'html.parser')

    # Identify the images we want
    html_imgs = soup_subpage.findAll("img", attrs={'class': re.compile(image_re_identifier)})

    for html_img in set(html_imgs):
        # Where the images are:
        img_src = html_img.get('src')

        # Get the name of the image from the URL
        full_img_name = img_src.split('/')[-1]
        name, ext = os.path.splitext(full_img_name)

        if name in closed_list:
            print('Skipped: ', name)
            continue

        closed_list.append(name)

        # Save the image in folder with its main extension
        urllib.urlretrieve(img_src, path+str(count)+ext)
