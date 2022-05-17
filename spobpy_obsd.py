from os import path

def write_audio_features(af):
    str = ''
    if float(af[0])  < .25:
        str += '[[' + 'LeastDanceable' +']]\n'
    elif float(af[0])  < .35:
        str += '[[' + 'LessDanceable' +']]\n'
    elif float(af[0])  > .65:
        str += '[[' + 'MoreDanceable' +']]\n'
    elif float(af[0])  > .75:
        str += '[[' + 'MostDanceable' +']]\n'
    else:
        str += '[[' + 'AverageDanceability' +']]\n'

    if float(af[1])  < .31:
        str += '[[' + 'LeastEnergy' +']]\n'
    elif float(af[1])  < .45:
        str += '[[' + 'LessEnergy' +']]\n'
    elif float(af[1])  > .8:
        str += '[[' + 'MoreEnergy' +']]\n'
    elif float(af[1])  > .9:
        str += '[[' + 'MostEnergy' +']]\n'
    else:
        str += '[[' + 'AverageEnergy' +']]\n'

    if float(af[2])  < -14:
        str += '[[' + 'LeastLoudness' +']]\n'
    elif float(af[2])  < -11:
        str += '[[' + 'LessLoudness' +']]\n'
    elif float(af[2])  > -5:
        str += '[[' + 'MoreLoudness' +']]\n'
    elif float(af[2])  > -3:
        str += '[[' + 'MostLoudness' +']]\n'
    else:
        str += '[[' + 'AverageLoudness' +']]\n'

    if int(af[3]) == 1:
        str += '[[' + 'Major' +']]\n'
    else:
        str += '[[' + 'Minor' +']]\n'

    if float(af[4])  < 0.07:
        str += '[[' + 'LowSpeechiness' +']]\n'
    else:
        str += '[[' + 'HighSpeechiness' +']]\n'

    if float(af[5])  < .12:
        str += '[[' + 'NotAcoustic' +']]\n'
    elif float(af[5])  < .3:
        str += '[[' + 'SomewhatAcoustic' +']]\n'
    else:
        str += '[[' + 'Acoustic' +']]\n'

    if float(af[6])  < .15:
        str += '[[' + 'NotInstrumental' +']]\n'
    elif float(af[6])  < .45:
        str += '[[' + 'SomewhatInstrumental' +']]\n'
    else:
        str += '[[' + 'Instrumental' +']]\n'

    if float(af[7])  < .2:
        str += '[[' + 'NotLive' +']]\n'
    elif float(af[7])  < .45:
        str += '[[' + 'SomewhatLive' +']]\n'
    else:
        str += '[[' + 'Live' +']]\n'

    if float(af[8])  < .3:
        str += '[[' + 'LowValence' +']]\n'
    elif float(af[8])  > .7:
        str += '[[' + 'HighValence' +']]\n'
    else:
        str += '[[' + 'AmbiguousValence' +']]\n'

    if float(af[9])  < 80:
        str += '[[' + 'LowestTempo' +']]\n'
    elif float(af[9])  < 100:
        str += '[[' + 'LowTempo' +']]\n'
    elif float(af[9])  > 145:
        str += '[[' + 'HighTempo' +']]\n'
    elif float(af[9])  > 160:
        str += '[[' + 'HighestTempo' +']]\n'
    else:
        str += '[[' + 'ModerateTempo' +']]\n'
    return str

def import_tracks(tracks_file_name,obsd_path):
    tracks_file = open(tracks_file_name, 'r')
    tracks_list = tracks_file.read().split('\n')[1::]
    tracks_list.pop()
    tracks = [track.split(',') for track in tracks_list]

    for track in tracks:
        file_name = track[0] + ' by ' + track[1] + ' on ' + track[3]
        file_name = file_name[0:min(len(file_name),200)]
        if(path.exists(obsd_path + file_name + '.md')):
            print('track already exists')
        else:
            file = open(obsd_path + file_name + '.md','w')
            file.write('name: ' + track[0] + '\n')
            file.write('artist: [[' + track[1] + ']]\n')
            file.write('album: [[' + track[3] + ' by ' + track[1] + ']]\n')
            file.write(write_audio_features(track[5:15]))
            file.write('\n#track')

def import_artists(artists_file_name,obsd_path):

    ar = open(artists_file_name, 'r')
    artists_list = ar.read().split('\n')[1::]
    artists_list.pop()
    artists = [artist.split(',') for artist in artists_list]

    for artist in artists:
        file_name = artist[0]
        if(path.exists(obsd_path + file_name + '.md')):
            print('artist already exists')
        else:
            file = open(obsd_path + file_name + '.md','w')
            file.write('artist: ' + artist[0] + '\n')
            file.write('genres:\n')
            if len(artist[1].split('|')) > 0:
                for genre in artist[1].split('|'):
                    if len(genre)>0:
                        if genre[0] == ' ':
                            genre = genre[1::]
                        file.write('[[' + genre + ']]\n')

                        if(path.exists(obsd_path + genre + '.md')):
                            print('genre already exists')
                        else:
                            genre_file = open(obsd_path + genre + '.md','w')
                            genre_file.write('#genre\n')

            file.write('related artists:\n')
            if len(artist[2].split('|')) > 0:
                for related in artist[2].split('|'):
                    if(len(related) > 0):
                        if related[0] == ' ':
                            related = related[1::]
                        file.write('[[' + related + ']]\n')
            file.write('\n#artist')

def import_albums(albums_file_name,obsd_path):
    al = open(albums_file_name, 'r')
    albums_list = al.read().split('\n')[1::]
    albums_list.pop()
    albums = [album.split(',') for album in albums_list]

    for album in albums:
        file_name = album[0] + ' by ' + album[1]
        file_name = file_name[0:min(len(file_name),200)]
        if(path.exists(obsd_path + file_name + '.md')):
            print('album already exists')
        else:
            file = open(obsd_path + file_name + '.md','w')
            file.write('album: ' + album[0] + '\n')
            file.write('artist: [[' + album[1] + ']]\n')
            file.write('\n#album')
