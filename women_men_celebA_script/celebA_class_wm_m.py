import os
import tqdm
import shutil
import pandas as pd


male_dir = "males/"
female_dir = "females/"
attrs_file = "list_attr_celeba.csv"
df_celebA_attrs = pd.read_csv(attrs_file)

m_ones = df_celebA_attrs[['image_id', 'Male']]

for _ in tqdm(m_ones):
    for img, male in zip(m_ones['image_id'], m_ones['Male']):
        if male == 1:
            shutil.move(male_dir+img)
        else:
            shutil.move(female_dir+img)
