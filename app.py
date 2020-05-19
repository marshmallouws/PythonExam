from flask import Flask, render_template, Markup, request, jsonify, abort
import pandas as pd
import data_handler
import json
from song_recommender import recommend_songs

app = Flask(__name__)

data = data_handler.clean_data()

songlist = data_handler.song_artist_to_string(data)
print(type(data))
print(len(songlist))
songlist = []
for idx, row in data.iterrows():
    title = row.loc["song_name"]
    artist = row.loc["artist_name"]
    songlist.append({"id": idx, "title": title, "artist": artist})


@app.route("/", methods=["GET"])
def show_frontpage():
    return render_template("index.html", songs=songlist)


@app.route("/", methods=["POST"])
def make_song_list():
    if not request.json:
        abort(400)
    songs = [int(i) for i in request.json]
    recommended = recommend_songs(songs)
    return (
        json.dumps(recommended, default=lambda o: o.__dict__, sort_keys=True, indent=4),
        200,
    )
