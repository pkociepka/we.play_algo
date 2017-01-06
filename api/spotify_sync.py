import sys
import os
sys.path.insert(0, os.getcwd())

import spotipy

from db.db_hook import DB_Connector
from domain.user import User
from domain.tracks import Track, Artist, Genre
from domain.playlist import Params


def user_saved_tracks(username, token):
    spotify = spotipy.Spotify(auth=token)
    search = spotify.current_user_saved_tracks()
    conn = DB_Connector("weplay")
    user_id = conn.find_user_id(username)

    user = User(user_id)
    user = User(user_id)
    # user_authors = set()
    # user_genres = set()
    # user_tracks = []
    for item in search['items']:
        track_data = item['track']
        track_genres = []
        track_authors = []
        for artist_data in track_data['artists']:
            track_authors.append(Artist(artist_data['id'], artist_data['name']))
            user.add_author(Artist(artist_data['id'], artist_data['name']))
        track_params_data = spotify.audio_features([track_data['id']])[0]
        track_params = Params(track_params_data['danceability'], track_params_data['energy'], track_params_data['instrumentalness'], track_params_data['valence'])
        user.add_track(Track(track_data['id'], track_data['name'], track_authors, track_genres, params=track_params))

    conn.put_user(user)
    conn.close()


def parse_users(user_names):
    conn = DB_Connector("weplay")
    res = []
    for user_name in user_names:
        user_id = conn.find_user_id(user_name)
        res.append(User(user_id))
    conn.close()
    return res
