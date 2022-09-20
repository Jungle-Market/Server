from flask import Flask, render_template, url_for, session
from flask import request
from flask import redirect

from db import db
market_db = db

app = Flask(__name__)
app.secret_key= b'_12341234'

@app.route("/")
def main():
    if "id" in session:
        return redirect(url_for('home'))
    else:
        return redirect(url_for('signin'))


@app.route("/home")
def home():
    db_items = market_db.items.find()
    return render_template("home.html",items=db_items)



@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        
        if market_db.users.find_one({'id' : id, 'pwd': pw}) :
            session['id'] = id
            return redirect(url_for('home'))
        else :
            return render_template("signin.html", login_success = False)
    else:
        return render_template("signin.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('signin'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")

    else:
        signup_id = request.form['signup_id']
        signup_pw = request.form['signup_pw']

        if signup_id == "" or signup_pw == "":
            return render_template("signup.html", signup_success = False)
        elif market_db.users.find_one({'id' : signup_id}):
            return render_template("signup.html", signup_same = True)
        else:
            market_db.users.insert_one({'id' : signup_id, 'pwd' : signup_pw})
            return render_template("signup.html", signup_success = True)


if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)
