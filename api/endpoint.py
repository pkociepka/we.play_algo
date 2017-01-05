import sys
import os
sys.path.insert(0, os.getcwd())

from algo.algorithm import Algorithm

from flask import Flask
from flask import request

import spotipy

app = Flask(__name__)

@app.route('/api/playlist', methods=['GET'])
def create_playlist():
    assert request.args['size'] == '20'
    assert request.args['users'] == 'u1,u2,u3'
    assert request.args['danceability'] == '0.1'
    assert request.args['instrumntalness'] == '0.2'
    assert request.args['energy'] == '0.3'
    assert request.args['valence'] == '0.4'
    return 'Hello, World!'

@app.route('/api/spotify/sync/<token>/<int:expiration>', methods=['POST'])
def sync_with_spotify(token, expiration):
    token = {"access_token": token,
             "token_type": "Bearer",
             "expires_at": expiration}
    spotify = spotipy.Spotify(auth=token)
    return spotify.search("Ravel", type='artist')
