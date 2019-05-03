import ast
import json
import pandas as pd


json_data = ""
with open("../rnb:hiphop1.txt") as f:
    json_data= f.readlines()

with open("./rnbbb(down-up).txt") as f:
    json_data2 = f.readlines()

data = [ast.literal_eval(item) for item in json_data]
data2 = [ast.literal_eval(item) for item in json_data2]

raw_data = data[0]
raw_data2 = data2[0]

df = pd.DataFrame(columns={"year", "artist", "albums"})

row_list = []
for i in range(len(raw_data)):
    row = {}
    row['year'] = raw_data[i]['year']
    row['artist'] = raw_data[i]['artist']
    row['albums'] = raw_data[i]['albums']
    
    row_list.append(row)

for i in range(len(raw_data2)):
    row = {}
    row['year'] = raw_data2[i]['year']
    row['artist'] = raw_data2[i]['artist']
    row['albums'] = raw_data2[i]['albums']
    
    row_list.append(row)


df = pd.DataFrame(row_list)

temp = []
for index, row in df.iterrows():
    if "&" in row['artist'] or "Featuring" in row['artist']:
        continue
    hold = []
    for album in row['albums']:
        track = row["albums"][album]
        hold.append(track)
    temp.append({row['artist']: hold})


temp2 = []
for item in temp:
    artist = ""
    all_lyrics = " "
    for key, value in item.items():
        artist = key
        for song in value[0]:
            all_lyrics += song

    temp2.append({artist:all_lyrics})