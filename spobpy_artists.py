import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests


def get_artists(tracks_file_name):
    tracks_list = open(tracks_file_name, 'r')
    tracks_rows = tracks_list.read().split('\n')[1::]
    tracks_rows.pop()
    tracks_artists_list = [track.split(',')[2] for track in tracks_rows]

    old_len = len(tracks_artists_list)
    tracks_artists_list = list(dict.fromkeys(tracks_artists_list))
    print(str(old_len-len(tracks_artists_list))+' duplicate artists removed')
    artists_list = []
    for row in tracks_artists_list:
        if '|' in row:
            row = row.replace(' ','').split('|')
            artists_list.extend(row)
        else:
            artists_list.append(row)
    return artists_list

def get_lines(artists_list,sp):

    split_num = 50

    req_num = int(len(artists_list)/split_num)
    if(len(artists_list)%split_num != 0):
        req_num += 1



    def process_list_as_string(item_list):
        item_list = str(item_list).replace(',','|')
        item_list = item_list.replace('[','')
        item_list = item_list.replace(']','')
        item_list = item_list.replace("'",'')
        return item_list


    lines = 'names,genres,related_artists\n'
    for i in range(req_num):
        start = split_num*i
        end = start+split_num
        info = sp.artists(artists_list[start:end])['artists']
        names_list = [artist['name'].replace(',','~!~').replace('/','~').replace('\\','~').replace(':','~')  for artist in info]
        genres_list = [process_list_as_string(artist['genres']) for artist in info]
        related_artists_list = []
        for artist in artists_list[start:end]:
            related_artists_list.append(process_list_as_string([artist_list['name'].replace(',','~!~').replace('/','~').replace('\\','~').replace(':','~')  for artist_list in sp.artist_related_artists(artist)['artists']]))
        print(str(round(float(i+1)/float(req_num),2)*100)+'%')

        full_list = [names_list[i] + ',' + genres_list[i] + ',' + related_artists_list[i] + '\n' for  i in range(len(names_list))]
        lines += ''.join(full_list)
    return lines
