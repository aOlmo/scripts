import requests
from bs4 import BeautifulSoup
import youtube_dl
import os
import pandas as pd

csvs_folder = 'CSVs/'
dl_to = 'playlists/'
failed_folder_name = 'failed/'
failed_file_name = 'failed-songs.txt'

def create_dir(dir_name):
    try:
        os.mkdir(dir_name)
        print("[+] New directory {} created".format(dir_name))
    except FileExistsError:
        print("[-] Directory {} already exists".format(dir_name))

def create_dirs(csv_files):
    print("[+] Getting all CSV files and creating their directories...")
    for f in csv_files:
        f = dl_to + f.split(".")[0]
        create_dir(f)


if __name__ == '__main__':
    csv_files = [file for file in os.listdir(csvs_folder) if file.endswith(".csv")]
    create_dirs(csv_files)
    create_dir(dl_to)

    print("")
    print("")

    for csv_f in csv_files:
        # Read CSV files and get list of tracks to download
        csv_f_path = csvs_folder+csv_f
        try:
            songs = pd.read_csv(csv_f_path)
        except:
            print("[-] Error while reading {} skipping this CSV".format(csv_f_path))
            continue
        playlist = csv_f.split('.')[0]
        total_songs = songs.shape[0]
        abs_path_save = os.getcwd()+"/"+dl_to+playlist+"/"
        failed_folder = abs_path_save+failed_folder_name
        failed_file = failed_folder+failed_file_name

        print("================ DOWNLOADING {} PLAYLIST ================".format(playlist))
        for i, row in songs.iterrows():

            track = row['Track']
            artist = row['Artist']
            vid_name = str(track)+" "+str(artist)

            print("\n[+] Downloading song {} -- {} {}/{}"
                  .format(vid_name, playlist, i+1, total_songs))

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
                # We get the first video on the list that is not an add
                if "watch?v=" in url and not "googleadservices" in url:
                    print(url)
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        try:
                            ydl.download([url])
                        except:
                            if not os.path.isdir(failed_folder):
                                create_dir(failed_folder)
                            print("\n\n[-] Failed to download {}. Continuing...".format(vid_name))
                            with open(failed_file, "a") as f:
                                f.write(vid_name+"\n")
                            break
                    break
