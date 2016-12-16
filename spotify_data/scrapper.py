import sys
import os
sys.path.insert(0, os.getcwd())

from random import sample

import spotipy
import spotipy.util as util

from domain.tracks import *
from domain.user import *
from db.db_hook import *


username = "erlangboy"
scope = 'user-top-read user-library-read user-follow-read'

token = util.prompt_for_user_token(username, scope,
                                    client_id='1f04ae7d7737482eb47594961c217f15',
                                    client_secret='c9751a4110444a67b141df640960eb60',
                                    redirect_uri='http://localhost:5000/api/redirect')

spotify = spotipy.Spotify(auth=token)

with open("artists.txt") as artists:
    artist_names = [x for x in artists.read().split("\n") if x]

artists = []
genres = []
tracks = []


def insert(lst, item):
    if item not in lst:
        lst.append(item)


def add_artist_by_name(artist_name):
    artist_data = spotify.search(artist_name, type='artist')['artists']['items'][0]
    artist = Artist(artist_data['id'], artist_data['name'])
    for g in artist_data['genres']:
        existing = [x for x in genres if x.name == g]
        if existing:
            artist.add_genre(existing[0])
        else:
            new_genre = Genre(len(genres) + 1, g)
            artist.add_genre(new_genre)
            insert(genres, new_genre)
    insert(artists, artist)
    return artist.id


def add_track(track):
    t_authors = []
    for t_a in t["artists"]:
        new_author = Artist(t_a["id"], t_a["name"])
        t_authors.append(new_author)
        insert(artists, new_author)

    t_album = spotify.album(t["album"]["id"])
    t_genres = []
    for t_g in t_album["genres"]:
        maybe_genre = [x for x in genres if x.name == t_g]
        if maybe_genre:
            t_genres.append(maybe_genre[0])
        else:
            new_genre = Genre(len(genres) + 1, t_g)
            t_genres.append(new_genre)
            insert(genres, new_genre)

    features = spotify.audio_features([track["id"]])[0]
    params = Params(features["danceability"], features["energy"], features["instrumentalness"], features['valence'])
    insert(tracks, Track(track["id"], track["name"], t_authors, t_genres, params))
    return track["id"]


for name in artist_names:
    print(name)
    artist_id = add_artist_by_name(name)
    for t in spotify.artist_top_tracks(artist_id)["tracks"]:
        add_track(t)

# print("\nTracks\n")
# [print(x) for x in tracks]
# print("\nArtists:\n")
# [print(a) for a in artists]
# print("\nGenres:\n")
# [print(g) for g in genres]

# users
users = []
for i in range(5):
    user = User(i)
    [user.add_genre(x) for x in sample(genres, 15)]  # 15
    [user.add_author(x) for x in sample(artists, 5)]  # 5
    [user.add_track(x) for x in sample(tracks, 50)]  # 50
    users.append(user)

conn = DB_Connector("mydb")
for g in genres:
    conn.put_genre(g)
for a in artists:
    conn.put_artist(a)
for t in tracks:
    conn.put_track(t)
for u in users:
    conn.put_user(u)
conn.close()
