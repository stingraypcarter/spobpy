import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests

def get_albums(tracks_file_name):
    tracks_list = open(tracks_file_name, 'r')
    tracks_rows = tracks_list.read().split('\n')[1::]
    tracks_rows.pop()
    albums_list = [track.split(',')[4] for track in tracks_rows]

    old_len = len(albums_list)
    albums_list = list(dict.fromkeys(albums_list))
    print(str(old_len-len(albums_list))+' duplicates removed')

    return albums_list

def get_lines(albums_list,sp):

    split_num = 20

    req_num = int(len(albums_list)/split_num)
    if(len(albums_list)%split_num != 0):
        req_num += 1

    lines = 'names,artists\n'
    for i in range(req_num):
        start = split_num*i
        end = start+split_num
        info = sp.albums(albums_list[start:end])['albums']
        names_list = [album['name'].replace(',','~!~').replace('/','~').replace('\\','~').replace(':','~')  for album in info]
        artists_names = [album['artists'][0]['name'].replace(',','~!~').replace('/','~').replace('\\','~').replace(':','~') for album in info]


        full_list = [names_list[i] + ',' + artists_names[i] + '\n' for  i in range(len(names_list))]
        lines += ''.join(full_list)
    return lines
