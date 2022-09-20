from flask import Flask, render_template, request
from db import db

app = Flask(__name__)
market_db = db


@app.route("/home")
def home():
    db_items = market_db.items.find()
    return render_template("home.html",items=db_items)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
