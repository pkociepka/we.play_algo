import sys
import os
sys.path.insert(0, os.getcwd())

from flask import Flask
from flask import request

from api.spotify_sync import *

from algo.algorithm import Algorithm, Params

app = Flask(__name__)

@app.route('/api/playlist', methods=['POST'])
def create_playlist():
    form = request.form
    users = form['users']
    params = Params(form['danceability'], form['energy'], form['hottness'], form['mood'])
    return ','.join([x.id for x in Algorithm(users).random(20)])

@app.route('/api/spotify/sync/<token>/<int:expiration>/<username>', methods=['POST'])
def sync_with_spotify(token, expiration, username):
    user_saved_tracks(username, token)
    return "OK"

@app.route('/api/redirect')
def redirect():
    return "Redirection!"
