import re
import ast
import json
import pandas as pd

''' This combines various files of data collected since the musixmatch API only allows for 2000 calls per
day when using for free'''

def read_file(filepath):
    data = ""
    with open(filepath) as f:
        data = f.readlines()
    return data

def convert_to_json(files):
    json_data = ""
    data = []
    
    for file in files:
        json_data = read_file(file)
        converted_form = [ast.literal_eval(item) for item in json_data]
        data.append(converted_form[0]) 
    return data

def get_rows(file_data):
    rows = []
    for j in range(len(file_data)):
        for i in range(len(file_data[j])):
            row = {}
            row['year'] = file_data[j][i]['year']
            row['artist'] = file_data[j][i]['artist']
            row['albums'] = file_data[j][i]['albums']
            rows.append(row)
    return rows

#remove features or collaborations
def remove_features(dataframe):
    no_features = []
    feat_re = "r[&,+\(\)/]"

    for index, row in dataframe.iterrows():
        if re.search(feat_re, row['artist']) or "Featuring" in row['artist']:
            continue
        hold = []
        for album in row['albums']:
            track = row["albums"][album]
            hold.append(track)
        no_features.append({row['artist']: hold})
    return no_features

#get all songs for an artist
def get_all_artists_songs(temp):    
    nextline_re = re.compile(r"\n")
    artist_songs = []
    for item in temp:
        each_song = []
        artist = ""
        for key, value in item.items():
            artist = key
            for song in value:
                for title, album_tracks in song.items():
                    tracks = nextline_re.sub(" ", album_tracks)
                    each_song.append(tracks)
        artist_songs.append({artist:each_song})
        
    return artist_songs

#write song to files: a song on a line 
def save_each_artist(all_songs, destination):
    for i in all_songs:
        try:
            for artist, all_tracks in i.items():
                filename = destination + artist + ".txt"
                with open(filename, "w") as text_file:
                    for track in all_tracks:
                        track = track + "\n"
                        text_file.write(track)
                print("Saved ", artist)
        except:
            continue

def combine_and_save(files, destination):
    data = convert_to_json(files)
    rows = get_rows(data)
    df = pd.DataFrame(rows)
    df_unique_artists = df.drop_duplicates(subset=['artist']) #select unique artists
    no_features = remove_features(df_unique_artists)
    artist_songs = get_all_artists_songs(no_features)
    save_each_artist(artist_songs, destination)


if __name__ == "__main__":
    rnb_hiphop_files = ["rnb:hiphop1.txt", "rnb:hiphop2.txt", "rnb:hiphop3.txt", "rnb:hiphop4.txt"] #example files
    destination = "genre/rnb/" #destination path
    combine_and_save(rnb_hiphop_files, destination)

