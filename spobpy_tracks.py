import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

def get_tracks(file_name):
    tracks_list = open(file_name, 'r')
    tracks_links = tracks_list.read().replace('\n',',').strip().split(',')
    tracks_list.close()
    tracks_links.pop()

    for track in tracks_links:
        if('/local/' in track):
            tracks_links.remove(track)

    return tracks_links

def artists_string(artists):
    urls = [artist['external_urls']['spotify'] for artist in artists]
    artists_string = str(urls).replace(',','|')
    artists_string = artists_string.replace('[','')
    artists_string = artists_string.replace(']','')
    artists_string = artists_string.replace("'",'')
    return artists_string


def get_lines(tracks_links,sp):
    lines = 'names,artists,artists_urls,album,album_url,danceability,energy,loudness,mode,speechiness,acousticness,instrumentalness,liveness,valence,tempo\n'
    split_num = 50
    req_num = int(len(tracks_links)/split_num)
    if(len(tracks_links)%split_num != 0):
        req_num += 1

    for i in range(req_num):
        start = split_num*i
        end = start+split_num
        info = sp.tracks(tracks_links[start:end],'US')['tracks']

        features = sp.audio_features(tracks_links[start:end])

        names = [track['name'].replace(',','~!~').replace('/','~').replace('\\','~').replace(':','~') for track in info]
        artists_names = [track['artists'][0]['name'].replace(',','~!~').replace('/','~').replace('\\','~').replace(':','~') for track in info]
        artists_urls = [artists_string(track['artists']) for track in info]
        album_names = [track['album']['name'].replace(',','~!~').replace('/','~').replace('\\','~').replace(':','~') for track in info]
        album_urls = [track['album']['external_urls']['spotify'] for track in info]

        danceability = [track['danceability'] for track in features]
        energy = [track['energy'] for track in features]
        loudness = [track['loudness'] for track in features]
        mode = [track['mode'] for track in features]
        speechiness = [track['speechiness'] for track in features]
        acousticness = [track['acousticness'] for track in features]
        instrumentalness = [track['instrumentalness'] for track in features]
        liveness = [track['liveness'] for track in features]
        valence = [track['valence'] for track in features]
        tempo = [track['tempo'] for track in features]


        full_list = [names[i] + ',' + artists_names[i] + ',' + artists_urls[i] + ',' + album_names[i] + ',' + album_urls[i] + ',' + str(danceability[i]) + ',' + str(energy[i]) + ',' + str(loudness[i]) + ',' + str(mode[i]) + ',' + str(speechiness[i]) + ',' + str(acousticness[i]) + ',' + str(instrumentalness[i]) + ',' + str(liveness[i]) + ',' + str(valence[i]) + ',' + str(tempo[i]) + '\n' for  i in range(len(names))]

        lines += ''.join(full_list)
    return lines
