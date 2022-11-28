from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route("/getauth")
def getauth():
    # Return an auth code so spotify API works
    return "ExampleAuth2rf3qv6n4w"

@app.route("/getplaylists")
def getplaylists():
    # Return an array of songs
    return []

@app.route("/getsongs")
def getsongs():
    # Return an array of songs
    return [{
        "name": "exampleName",
        "artist": "exampleArtist"
    },
    {
        "name": "exampleName",
        "artist": "exampleArtist"
    }]

if __name__ == "__main__":
  app.run()