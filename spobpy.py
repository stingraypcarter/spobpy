import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import sys
import requests
import spobpy_tracks
import spobpy_artists
import spobpy_albums
import spobpy_obsd


def write_csv(file_name,lines):
    file = open(file_name,'w')
    file.write(lines)
    file.close()

if __name__ == "__main__":
    input_text = sys.argv[1]
    obsd_path = sys.argv[2]
    # input_text = 'tracks.txt'
    # obsd_path = '/Users/ray/Desktop/Music_Analysis/'
    hidden_obsd_path = obsd_path + '.obsidian/'
    audio_feature_path = obsd_path + '_audiofeatures/'
    os.mkdir(audio_feature_path)
    os.mkdir(hidden_obsd_path)

    creds = open('client_credentials.txt', 'r')
    id, secret = creds.readlines()
    id = id[:-1]
    print(id)
    # print(secret)
    client_credentials_manager = SpotifyClientCredentials(client_id=id,client_secret=secret)


    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


    track_csv = obsd_path + 'tracks_info.csv'
    artist_csv = obsd_path + 'artists_info.csv'
    album_csv = obsd_path + 'albums_info.csv'

    tracks = spobpy_tracks.get_tracks(input_text)
    tracks_lines = spobpy_tracks.get_lines(tracks,sp)

    write_csv(track_csv,tracks_lines)

    artists = spobpy_artists.get_artists(track_csv)
    artists_lines = spobpy_artists.get_lines(artists,sp)

    write_csv(artist_csv,artists_lines)

    albums = spobpy_albums.get_albums(track_csv)
    albums_lines = spobpy_albums.get_lines(albums,sp)

    write_csv(album_csv,albums_lines)

    spobpy_obsd.import_tracks(track_csv,obsd_path)
    spobpy_obsd.import_artists(artist_csv,obsd_path)
    spobpy_obsd.import_albums(album_csv,obsd_path)

    audio_feature_string = 'Acoustic.md,LeastLoudness.md,MoreDanceable.md\
    ,AmbiguousValence.md,LessDanceable.md,MoreEnergy.md\
    ,AverageDanceability.md,LessEnergy.md,MoreLoudness.md\
    ,AverageEnergy.md,LessLoudness.md,MostDanceable.md\
    ,AverageLoudness.md,Live.md,MostEnergy.md\
    ,HighSpeechiness.md,LowSpeechiness.md,MostLoudness.md\
    ,HighTempo.md,LowTempo.md,NotAcoustic.md\
    ,HighValence.md,LowValence.md,NotInstrumental.md\
    ,HighestTempo.md,LowestTempo.md,NotLive.md\
    ,Instrumental.md,Major.md,SomewhatAcoustic.md\
    ,LeastDanceable.md,Minor.md,SomewhatInstrumental.md\
    ,LeastEnergy.md,ModerateTempo.md,SomewhatLive.md'

    audio_features = audio_feature_string.split(',')
    for au in audio_features:
        file = open(audio_feature_path + au.strip(),'w')
        file.write('#audiofeature')
        file.close()

    graph_json = '{"collapse-filter":true,"search":"- #audiofeature","showTags":false,"showAttachments":false,"hideUnresolved":false,"showOrphans":true,"collapse-color-groups":false,"colorGroups":[{"query":"#track","color":{"a":1,"rgb":14701138}},{"query":"#album","color":{"a":1,"rgb":15662848}},{"query":"#artist","color":{"a":1,"rgb":16746496}},{"query":"#genre","color":{"a":1,"rgb":5431378}},{"query":"#audiofeature","color":{"a":1,"rgb":5431473}},{"query":"","color":{"a":1,"rgb":5419488}}],"collapse-display":true,"showArrow":false,"textFadeMultiplier":0,"nodeSizeMultiplier":1,"lineSizeMultiplier":1,"collapse-forces":true,"centerStrength":0.518713248970312,"repelStrength":10,"linkStrength":1,"linkDistance":250,"scale":0.7683174228123679,"close":true}'

    graph_data = open(hidden_obsd_path + 'graph.json','w')
    graph_data.write(graph_json)
    graph_data.close()
