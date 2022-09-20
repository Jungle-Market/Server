from flask import Flask, render_template, request
from db import db

app = Flask(__name__)
market_db = db


@app.route("/home")
def home():
    items = market_db.items.find()
    for i in items:
        print(i)
    return render_template("home.html")


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
