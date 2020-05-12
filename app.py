from flask import Flask, render_template, Markup, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def show_frontpage():
    return render_template("index.html")
