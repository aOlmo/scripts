import requests
from bs4 import BeautifulSoup
import youtube_dl
import os
import pandas as pd

csvs_folder = 'CSVs/'
dl_to = 'playlists/'

try:
    # Create target Directory
    os.mkdir(dl_to)
    print("[+] New directory {} created".format(dl_to))
except FileExistsError:
    print("[-] Directory {} already exists".format(dl_to))

def create_dirs(csv_files):
    print("[+] Getting all CSV files and creating their directories...")
    for csv_f in csv_files:
        csv_f = dl_to + csv_f.split(".")[0]
        try:
            # Create target Directory
            os.mkdir(csv_f)
            print("[+] New directory {} created".format(csv_f))
        except FileExistsError:
            print("[-] Directory {} already exists".format(csv_f))

csv_files = [file for file in os.listdir(csvs_folder) if file.endswith(".csv")]
create_dirs(csv_files)

print("")
print("")

for csv_f in csv_files:
    # Read CSV files and get list of tracks to download
    csv_f_path = csvs_folder+csv_f
    songs = pd.read_csv(csv_f_path)
    folder_name = csv_f.split('.')[0]
    total_songs = songs.shape[0]
    abs_path_save = os.getcwd()+"/"+dl_to+folder_name+"/"

    for i, row in songs.iterrows():
        print("\n[+] Downloading song {}/{} for tracklist {}"
              .format(i+1, total_songs, folder_name))

        track = row['Track']
        artist = row['Artist']
        vid_name = track +" "+ artist

        vid_query = vid_name.replace("\t"," ").replace(" ","+")
        r = requests.get("https://www.youtube.com/results?search_query={}".format(vid_query))
        soup = BeautifulSoup(r.content, 'html.parser')


        ydl_opts = {
            'writethumbnail': True,
            'outtmpl': '/'+abs_path_save+'%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [
                {'key': 'FFmpegExtractAudio',
                 'preferredcodec': 'mp3',
                 'preferredquality': '192'},
                {'key': 'EmbedThumbnail',},
            ]
        }

        for vid in soup.findAll(attrs={'class': 'yt-uix-tile-link'}):
            url = 'https://www.youtube.com' + vid['href']
            print(url)
            # We get the first video on the list
            if "watch?v=" in url:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    try:
                        ydl.download([url])
                    except:
                        print("\n\n[-] Failed to download {}. Continuing..."
                              .format(vid_name))
                        break
                break



