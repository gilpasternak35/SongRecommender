from flask import Flask
from flask import request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/getauth")
def getauth():
    # Return an auth code so spotify API works
    return "ExampleAuth2rf3qv6n4w"

@app.route("/getplaylists")
def getplaylists():
    username = request.args.get("username")
    # Return an array of songs
    return {"data": ["Test Playlist 1"]}

@app.route("/getsongs")
def getsongs():
    username = request.args.get("username")
    playlist = request.args.get("playlist")
    # Return an array of songs
    return {"data": [{
        "name": "exampleName",
        "artist": "exampleArtist"
    },
    {
        "name": "exampleName2",
        "artist": "exampleArtist2"
    }]}
    
if __name__ == "__main__":
  app.run()