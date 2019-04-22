from flask import Flask, render_template, redirect, url_for, flash, request, Session
from datetime import datetime
from RegistrationForm import RegistrationForm
import sqlite3 as sql

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World! <br>" + str(datetime.now())

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST':
        #user = User(form.username.data, form.email.data)
        try:
            username = form.username.data
            email = form.email.data
            with sql.connect("pythonsqlite.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO User (username,email) VALUES (?, ?)",(username, email) )
                con.commit()
                print("inserted into table")
                msg = "Record successfully added"


        except:
            print("Connection Error")
            con.rollback()
            msg = "error in insert operation"

        #db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == "__main__":
    sess = Session()
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run()
