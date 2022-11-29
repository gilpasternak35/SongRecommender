from flask import Flask, render_template
from flask import request
from flask_cors import CORS
import requests

import configparser

import spotipy
import spotipy.oauth2 as oauth2
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

app = Flask(__name__)
CORS(app)

@app.route("/getrecommendations", methods = ['POST'])
def getrecommendations():
    songs = request.args.get("songs")
    return [{
        "name": "Skyfall",
        "artist": "Bravo"
    }, {
        "name": "Drama",
        "artist": "AJR"
    }, {
        "name": "Believer",
        "artist": "Imagine Dragons"
    }, ]

@app.route("/callback")
def callback():
    return render_template('loginFin.html')
    
if __name__ == "__main__":
  app.run()