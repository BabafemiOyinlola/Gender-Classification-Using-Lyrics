import csv
import json
import requests
from musixmatch import Musixmatch
from bs4 import BeautifulSoup
import lyricsgenius as genius
from genuis_token import token
from musix import api_key_6


api = genius.Genius(token)
musixmatch = Musixmatch(api_key_6)

#store song, year and artist of song
def get_music_list(year, soup, music):
    for row in soup.select('tbody tr'):
        row_text = [x.text for x in row.find_all('td')]
        if len(row_text) > 2:
            song = row_text[1].strip()
            artist = row_text[2].strip()
            music.append({'year': year, 'song': song, 'artist': artist})

#change url for different years
def url(year, genre_path):
    base_url = ("https://www.billboard.com/archive/charts/%d/" % (year))
    url = base_url + genre_path
    req = requests.get(url)
    soup = BeautifulSoup(req.text, "html.parser")
    return soup

#iterate through years needed
def get_song_details(start, end, genre_path, genre):
    print("Retriving %s ....." %(genre))
    music = []
    for i in range(start, end):
        soup = url(i, genre_path)
        get_music_list(i, soup, music)

    filename = "billboard_top_%s_(%d_%d).json" % (genre, start, end-1)  #save song details
    with open(filename, 'w') as f:
        json.dump(music, f)
    return music

def get_artists_albums(filepath, filename):
    filename = filename + ".json"
    count = 0
    details = json.load(open(filepath))

    artists_and_track = []

    # for item in range(len(details), 0, -1):
    for i in range(len(details)-1, 0, -1):
        item = details[i]
        if len(artists_and_track) > 0:
            artists = [key['artist'] for key in artists_and_track]
            if item['artist'] in artists:
                continue
        try:
            musixmatch_song_match = musixmatch.matcher_track_get(q_track=item['song'], q_artist=item['artist'])['message'] #match song in musixmatch database
            if(musixmatch_song_match['body'] == "" or (musixmatch_song_match['header']['status_code'] != 200)):
                print(str(musixmatch_song_match['body']))
                print("Error: ", musixmatch_song_match['header']['status_code'])

                if(musixmatch_song_match['header']['status_code'] == 404):
                    continue
            
                file1 = open("pop2.txt","w")# save 
                file1.write(str(artists_and_track)) 
                file1.close()
         
                print("Saved")
                break

            artist_id = musixmatch_song_match['body']['track']['artist_id'] #get artist_id
            artist_album_list = musixmatch.artist_albums_get(artist_id=artist_id, g_album_name=1, s_release_date="desc", page=1, page_size=100)['message']['body']['album_list']
            albums = set((album['album']['album_name'], album['album']['album_id']) for album in artist_album_list)
            item['albums'] = {}
            #add track to album
            album_temp = {}
            collected_album_id = []
            for album in albums:
                try:
                    temp = {}
                    if album[1] in collected_album_id: 
                        print("Album tracks already retrived")
                        continue

                    collected_album_id.append(album[1])
                    tracks = musixmatch.album_tracks_get(album_id=album[1], page=1, page_size=100, album_mbid="")['message']['body']['track_list'] #get all tracks in album
                    #get lyrics for all tracks:
                    for track in tracks:
                        try:
                            track_id = track['track']['track_id']
                            track_name = track['track']['track_name']
                            track_lyrics = musixmatch.track_lyrics_get(track_id = track_id)['message']['body']['lyrics']['lyrics_body'] #get lyrics for track
                            temp[track_name] = track_lyrics   #save track name and corresponding lyrics
                        except Exception:
                            print("Exception thrown getting tracks ", item['artist'])
                            continue
                        album_temp[album] = temp  #save each track for each album
                except Exception:
                    print("Exception thrown in albulm")
                    continue
            item['albums'] = album_temp
            artists_and_track.append(item)
            # count = i
            count = i 
            print(str(count) + " " + item['artist'])
        except Exception as e:
            print(e)
            print("Exception thrown ", item['artist'])
            continue

    file1 = open("pop2backup.txt","w")#write mode 
    file1.write(str(artists_and_track)) 
    file1.close()

    with open(filename, 'w') as f:
        json.dump(artists_and_track, f) #save details

    return artists_and_track


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



# rnb_hiphop  = get_song_details(1980, 2019, "r-b-hip-hop-songs", "rnb_hip-hop")
# pop = get_song_details(1980, 2019, "adult-contemporary", "pop-adult-contemporary")
# country = get_song_details(1980, 2019, "country-songs", "country")


# all_rnb = get_artists_albums("/Users/oyinlola/Desktop/MSc Data Science/LENT TERM/SCC 413 - Applied Data Mining/Research Projects/billboard_top_rnb_hip-hop_(1980_2018).json", "All_Rnb")
all_pop = get_artists_albums("/Users/oyinlola/Desktop/MSc Data Science/LENT TERM/SCC 413 - Applied Data Mining/Research Projects/billboard_top_pop-adult-contemporary_(1980_2018).json", "All_pop2")
all_country = get_artists_albums("/Users/oyinlola/Desktop/MSc Data Science/LENT TERM/SCC 413 - Applied Data Mining/Research Projects/billboard_top_country_(1980_2018).json", "All_country")




filename = "pop1.json"   #save song details
with open(filename, 'w') as f:
    json.dump(all_pop, f)



file1 = open("pop111.txt","w")#write mode 
file1.write(str(all_pop)) 
file1.close()

print("Done")
