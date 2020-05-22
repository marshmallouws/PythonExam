from flask import Flask, render_template, Markup, request, jsonify, abort
from flask_cors import CORS
import pandas as pd
import data_handler
import json
from song_recommender import recommend_songs
from scraper import search2

app = Flask(__name__)
CORS(app)

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
    liked_songs = [int(i) for i in request.json[0]]
    disliked_songs = [int(i) for i in request.json[1]]
    recommended = recommend_songs(liked_songs, disliked_songs)
    return (
        json.dumps(recommended, default=lambda o: o.__dict__, sort_keys=True, indent=4),
        200,
    )


@app.route("/suggest", methods=["GET"])
def autocomplete():
    search = request.args.get("q")
    results = data[
        data["song_name"].str.contains(search, case=False)
        | data["artist_name"].str.contains(search, case=False)
    ]
    songs = [
        {"label": song.loc["song_name"] + " - " + song.loc["artist_name"], "value": idx}
        for idx, song in results.iterrows()
    ]
    return jsonify(matching_results=songs)


@app.route("/songinfo", methods=["POST"])
def song_info():
    song_info = data.iloc[int(request.json)]
    result = search2(song_info)
    return jsonify(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
