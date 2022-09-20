from flask import Flask, render_template, url_for, session
from flask import request
from flask import redirect
import re
import time

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
        signup_check_pw = request.form['signup_check_pw']
        signup_name = request.form['signup_name']
        signup_nickname = request.form['signup_nickname']

        p = re.compile("^[a-zA-Z0-9+-\_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

        if signup_id == "" or signup_pw == "" or signup_name == "" or signup_nickname == "":
            return render_template("signup.html", signup_success = False)
        elif not p.findall(signup_id):
            return render_template("signup.html", signup_check_id = False)
        elif market_db.users.find_one({'id' : signup_id}):
            return render_template("signup.html", signup_same = True)
        elif signup_pw != signup_check_pw:
            return render_template("signup.html", signup_same_pw = True)
        else:
            market_db.users.insert_one({'id' : signup_id, 'pwd' : signup_pw, 'name' : signup_name, 'nickname' : signup_nickname})
            return render_template("signup.html", signup_success = True)

@app.route('/register', methods=['POST', 'GET'])
def file_upload():
    current_time = str(time.time()).replace('.','')
    if request.method == 'POST':
        uploaded_file = request.files["myfile"]
        uploaded_title = request.form["title"]
        uploaded_text = request.form["text"]
        uploaded_count = request.form["count"]
        uploaded_url = "img/{}.jpeg".format(uploaded_title+current_time)
        uploaded_file.save(
            "static/"+uploaded_url)
        data = {'title': uploaded_title, 'user':"user",'count':int(uploaded_count),'text': uploaded_text,
                'url': uploaded_url, "reviews": []}
        db.items.insert_one(data)
        return render_template('register.html')
    else:
        return render_template('register.html', name="jinja_test")

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)
