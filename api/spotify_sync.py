import sys
import os
sys.path.insert(0, os.getcwd())

import spotipy


def get_user_saved_tracks(username, token):
    spotify = spotipy.Spotify(auth=token)
    search = spotify.current_user_saved_tracks()
