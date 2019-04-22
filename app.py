from flask import Flask, render_template, redirect, url_for, flash, request, Session, g
from datetime import datetime
from RegistrationForm import RegistrationForm
import sqlite3 as sql

app = Flask(__name__)
sess = Session()


@app.route("/")
def hello():
    if 'username' not in sess:
        return "Hello World! " + "<br>" + str(datetime.now())
    return "Hello " + sess['username'] + "<br>" + str(datetime.now())


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        # user = User(form.username.data, form.email.data)
        try:
            username = form.username.data
            email = form.email.data
            with sql.connect("pythonsqlite.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO User (username,email) VALUES (?, ?)", (username, email))
                con.commit()
                print("inserted into table")
                msg = "Record successfully added"


        except:
            print("Connection Error")
            con.rollback()
            msg = "error in insert operation"

        # db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = query_db('select * from User where username = ?',
                        [request.form['username']], one=True)
        if user is None:
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
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
