from flask import Flask, render_template, redirect, url_for, flash, request
from datetime import datetime
from RegistrationForm import RegistrationForm

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello World! <br>" + str(datetime.now())

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        #db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

if __name__ == "__main__":
    app.run()
