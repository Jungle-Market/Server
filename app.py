from flask import Flask, render_template, url_for, session
from flask import request
from flask import redirect
from flask import flash
from bson import ObjectId
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
    if "id" in session:
        db_items = market_db.items.find()
        return render_template("home.html",items=db_items)
    else:
        return redirect(url_for('signin'))


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        
        if market_db.users.find_one({'id' : id, 'pwd': pw}) :
            session['nickname'] = market_db.users.find_one({'id': id})['nickname']
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
def register():
    if "id" in session:
        if request.method == 'POST':
            current_time = str(time.time()).replace('.','')
            
            item_title = request.form["title"]
            item_text = request.form["text"]
            item_count = request.form["count"]
            item_image = request.files["myfile"]
            #확장자 파싱
            item_image_format = item_image.filename.split('.')[1]
            item_image_url = "img/items/{}".format(item_title+current_time + "." + item_image_format)
            #아이템 이미지 저장
            item_image.save(
                "static/"+item_image_url)
            item_data = {'title': item_title, 'user':{'id':session['id'],'nickname':session['nickname']},'count':int(item_count),'text': item_text,
                    'url': item_image_url, "reviews": []}
            db.items.insert_one(item_data)
            return redirect(url_for('home'))
        else:
            return render_template('register.html')
    else:
        return redirect(url_for('signin'))

@app.route('/desc/<string:id>', methods=['POST', 'GET'])
def desc(id):
    if request.method == 'POST':
        selected_item = market_db.items.find_one({'_id': ObjectId(id)})
        current_count = selected_item['count']
        #잔여수량 확인
        if current_count==0:
            selected_title = selected_item['title']
            flash("죄송합니다 {}의 재고가 모두 소진되었습니다.".format(selected_title))
            return render_template("desc.html", item=selected_item)
        else:
            comment = request.form["comment"]
            db.items.update_one({'_id': ObjectId(id)}, {'$push': {'reviews': {
                                "nickname": session['nickname'], "text": comment}}},)
            db.items.update_one({'_id': ObjectId(id)}, {
                            '$set': {'count': current_count-1}})
            selected_item = market_db.items.find_one({'_id': ObjectId(id)})
            return render_template("desc.html", item=selected_item)
    print(id)
    selected_item = market_db.items.find_one({'_id': ObjectId(id)})
    return render_template("desc.html",item=selected_item)

if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)
