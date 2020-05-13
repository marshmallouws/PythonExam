from flask import Flask, render_template, Markup, request
import pandas as pd

app = Flask(__name__)

df = pd.read_csv("data/song_data.csv")
songs = df.iloc[:, 0]


@app.route("/", methods=["GET", "POST"])
def show_frontpage():
    return render_template("index.html", songs=songs)
