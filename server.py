from flask import Flask, render_template
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/getrecommendations", methods = ['POST'])
def getrecommendations():
    songs = request.args.get("songs")
    return {"data": [{
        "name": "Skyfall",
        "artist": "Bravo"
    }, {
        "name": "Drama",
        "artist": "AJR"
    }, {
        "name": "Believer",
        "artist": "Imagine Dragons"
    }, ]}

@app.route("/callback")
def callback():
    return render_template('loginFin.html')
    
if __name__ == "__main__":
  app.run()