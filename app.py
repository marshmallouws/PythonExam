from flask import Flask, render_template, Markup, request, jsonify, abort
import pandas as pd
import data_handler

app = Flask(__name__)

df = pd.read_csv("data/song_info.csv")
data = data_handler.clean_data(df)

songlist = data_handler.song_artist_to_string(data)
print(type(data))
print(len(songlist))
songlist = []
for idx, row in data.iterrows():
    title = row.loc["song_name"]
    artist = row.loc["artist_name"]
    idx
    songlist.append({"id": idx, "title": title, "artist": artist})


@app.route("/", methods=["GET"])
def show_frontpage():
    return render_template("index.html", songs=songlist)


@app.route("/", methods=["POST"])
def make_song_list():
    if not request.json:
        abort(400)
    songs = {"songs": request.json["songs"]}
    print(songs)
    return jsonify(songs), 201
