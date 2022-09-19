from flask import Flask,render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html',name="jinja_test")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)