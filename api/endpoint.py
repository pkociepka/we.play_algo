import sys
import os
sys.path.insert(0, os.getcwd())

from flask import Flask
from flask import request

from api.spotify_sync import *

app = Flask(__name__)

@app.route('/api/playlist', methods=['POST'])
def create_playlist():
    return ','.join(['0aym2LBJBk9DAYuHHutrIl', '0hCB0YR03f6AmQaHbwWDe8', '0iOZM63lendWRTTeKhZBSC', '0JQuwvPum9mcIx9yOTq8K9'])

@app.route('/api/spotify/sync/<token>/<int:expiration>/<username>', methods=['POST'])
def sync_with_spotify(token, expiration, username):
    get_user_saved_tracks(username, token)
    return "OK"

@app.route('/api/redirect')
def redirect():
    return "Redirection!"
