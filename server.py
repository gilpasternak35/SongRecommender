from flask import Flask, render_template
from flask import request
from flask_cors import CORS
import json
from generate_predictions import generate_predictions

app = Flask(__name__)
CORS(app)

@app.route("/getrecommendations")
def getrecommendations():
    songs = json.loads(request.args.get("songs"))
    f = open('data_train.json')
    data = json.load(f)
    pred = generate_predictions(songs, data)
    structuredData = []
    for i in pred:
        structuredData.append({
            "name": i[0],
            "artist": i[1],
        })
    return {"data": structuredData}

@app.route("/callback")
def callback():
    return render_template('loginFin.html')
    
if __name__ == "__main__":
  app.run()