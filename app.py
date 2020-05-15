from flask import Flask, render_template, Markup, request
import pandas as pd
import data_handler

app = Flask(__name__)

df = pd.read_csv("data/song_info.csv")
data = data_handler.clean_data(df)
songlist = data_handler.song_artist_to_string(data)


@app.route("/", methods=["GET"])
def show_frontpage():
    return render_template("index.html", songs=songlist)


@app.route("/", methods=["POST"])
def process():
    p = request.form["list_s"]
    print(p)
    return p