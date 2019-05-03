import csv
import json
import requests
from bs4 import BeautifulSoup
import lyricsgenius as genius
from genuis_token import token

api = genius.Genius(token)

#store song, year and artist of song
def get_music_list(year, soup, music):
    for row in soup.select('tbody tr'):
        row_text = [x.text for x in row.find_all('td')]
        if len(row_text) > 2:
            song = row_text[1].strip()
            artist = row_text[2].strip()
            music.append({'year': year, 'song': song, 'artist': artist})

#change url for different years
def url(year):
    base_url = ("https://www.billboard.com/archive/charts/%d/r-b-hip-hop-songs" % (year))
    req = requests.get(base_url)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup

#iterate through years needed
def get_song_details(start, end):
    music = []
    for i in range(start, end):
        soup = url(i)
        get_music_list(i, soup, music)

    filename = "billboard_top_songs_(%d_%d).json" % (start, end-1)  #save song details
    with open(filename, 'w') as f:
        json.dump(music, f)
    return music

#update music json with lyrics
def get_lyrics(music):
    try:
        for song in music:
            lyrics = api.search_song(song['song'], song['artist']) 
            if lyrics == None:
                continue
            song['lyrics'] = lyrics.lyrics
            print("Year: ",song['year'])
    except:
        print ("%s not found" % (song['song']))

    filename = "billboard_top_songs_lyrics_new.json"   #save song details
    with open(filename, 'w') as f:
        json.dump(music, f)
    return music


import re
import ftfy
import pandas as pd

df = pd.read_json("billboard_top_rnb-hiphop.json")

sections_re = re.compile(r"(\[)?\[(.*?)\](\])?")#anything in square bracket
par_re = re.compile(r"\(.\)")
verse_re = re.compile(r"([\d][a-z][a-z][\s])?[V|v]erse(:)?[\s](\w.)?")
repeat_re = re.compile(r"(\n)?[R|r]epeat[A-Za-z .\(\)\d]+")


def preprocess(text):
    p_text = sections_re.sub("", text)
    p_text = par_re.sub("", p_text)
    a = repeat_re.match(p_text)
    p_text = verse_re.sub("", p_text)
    p_text = repeat_re.sub("", p_text)
    p_text = ftfy.fix_text(p_text)
    return p_text.lower()


def remove_artist_name(artist, lyrics):
    pattern = r"(\n)?"+artist+"[a-z .\(\)\d]+"
    artist_re = re.compile(pattern)
    p_text = artist_re.sub("", lyrics)
    return p_text



# import nltk
# from nltk.corpus import stopwords
# a = stopwords.words('english')








# data_clean = df.copy()

# for index, row in data_clean.iterrows():
#     print(row)
#     print(data_clean.loc[index, 'lyrics'])
#     data_clean.loc[index, 'lyrics'] = preprocess(data_clean.loc[index, 'lyrics'])
#     print(data_clean.loc[index, 'lyrics'])
#     artist = data_clean.loc[index, 'artist'] 
#     lyrics = data_clean.loc[index, 'lyrics'] 
#     check = data_clean.loc[index, 'artist'] in data_clean.loc[index, 'lyrics']
#     if data_clean.loc[index, 'artist'] in data_clean.loc[index, 'lyrics']:
#         print(data_clean.loc[index, 'lyrics'])
#         print("\n\n\n\n\n")
#         print(data_clean.loc[index, 'artist'])
#         data_clean.loc[index, 'lyrics'] = remove_artist_name(data_clean.loc[index, 'artist'], data_clean.loc[index, 'lyrics'])
        








music = get_song_details(1980, 2019)

lyrics = get_lyrics(music)

print("Done")


