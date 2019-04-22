from flask import Flask, render_template, redirect, url_for, flash, request, Session, g
from datetime import datetime
from RegistrationForm import RegistrationForm
import sqlite3 as sql
import pyrebase
from werkzeug.utils import secure_filename
import os
import random

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


app = Flask(__name__)
app.secret_key = 'firesquad_intern_match'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
sess = Session()


config = {
    "apiKey": "AIzaSyDYVo10h_DYJh-zmxCU4wp3AAjOesQ_T4c",
    "authDomain": "firesquad-37ddd.firebaseapp.com",
    "databaseURL": "https://firesquad-37ddd.firebaseio.com",
    "projectId": "firesquad-37ddd",
    "storageBucket": "firesquad-37ddd.appspot.com",
    "messagingSenderId": "987773115186"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database=firebase.database()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file(username=''):
    if request.method == 'POST' and request.form['btn'] == 'upload':
        print("in upload methiod ")
    # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            print("no files ")
            flash('No file part')
        # return redirect(request.url)
        file = request.files['file']
        print("the file ", file)
    # if user does not select file, browser also
    # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            # return redirect(request.url)
        if file and allowed_file(file.filename):
            random_no = random.randint(0, 10000)
            filename =  str(random_no) +  '.' + file.filename.rsplit('.', 1)[1].lower()
            sess['photo_id'] = filename
            # secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            # filename=filename))
    form = RegistrationForm(request.form)
    return render_template('register.html', form=form)



@app.route("/")
def hello():
    #database.child("user").set("test")
    if 'username' not in sess:
        return "Hello World! " + "<br>" + str(datetime.now())
    return "Hello " + sess['username'] + "<br>" + str(datetime.now())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and request.form['btn'] == 'Register':
        # user = User(form.username.data, form.email.data)
        try:
            username = form.username.data
            email = form.email.data
            photo_id = sess['photo_id']
            database.child("User").child(username).child("name").set(username)
            database.child("User").child(username).child("pic").set(photo_id)

            #with sql.connect("pythonsqlite.db") as con:
            #    cur = con.cursor()
            #    cur.execute("INSERT INTO User (username,email) VALUES (?, ?)", (username, email))
            #    con.commit()
            #    print("inserted into table")
            #    msg = "Record successfully added"
            #upload_file(username)


        except:
            print("Connection Error")
            #con.rollback()
            msg = "error in insert operation"

        # db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        user = database.child("User").child(request.form['username']).get()
        print("username:"+str(user.val()))
        #user = query_db('select * from User where username = ?',
        #                [request.form['username']], one=True)
        if user.val() is None:
            print('No such user')
        else:
            print(request.form['username'] + ' exists')
            sess['username'] = request.form['username']
            return redirect(url_for('hello'))
    return render_template('login.html', error=error)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect("pythonsqlite.db")
    return db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


if __name__ == "__main__":
    app.run()
