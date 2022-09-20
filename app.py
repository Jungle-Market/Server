from flask import Flask, render_template, jsonify, request, redirect, url_for
from db import db, MongoClient
import time

app = Flask(__name__)
client = MongoClient('localhost', 27017)

@app.route('/register', methods=['POST', 'GET'])
def file_upload():
    current_time = str(time.time()).replace('.','')
    if request.method == 'POST':
        uploaded_file = request.files["myfile"]
        uploaded_title = request.form["title"]+current_time
        uploaded_text = request.form["text"]
        uploaded_count = request.form["count"]
        uploaded_file.save(
            "static/img/{}.jpeg".format(uploaded_title))
        data = {'title': uploaded_title, 'user':"user",'count':int(uploaded_count),'text': uploaded_text,
                'url': "img/{}.jpeg".format(uploaded_title), "comments": [{"":""}]}
        db.register.insert_one(data)
        return render_template('register.html')
    else:
        return render_template('register.html', name="jinja_test")


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
