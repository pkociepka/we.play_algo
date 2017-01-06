import sys
import os
sys.path.insert(0, os.getcwd())

from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
import json

from api.spotify_sync import *
from algo.algorithm import Algorithm, Params

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/playlist', methods=['POST'])
def create_playlist():
    form = json.loads(request.data.decode("utf-8"))
    users = parse_users(form['users'])
    params = Params(form['dancability'], form['energy'], form['hottness'], form['mood'])
    raw_response = ','.join([x.id for x in Algorithm(users).random(20)])
    response = Response()
    response.set_data(raw_response)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/api/spotify/sync/<token>/<int:expiration>/<username>', methods=['POST'])
def sync_with_spotify(token, expiration, username):
    user_saved_tracks(username, token)
    return "OK"

@app.route('/api/redirect')
def redirect():
    return "Redirection!"
