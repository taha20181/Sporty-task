# flask import
from flask import Flask, redirect, render_template, session, flash, url_for, request, jsonify
from flask_pymongo import PyMongo

# os import for env variable
import os

# import for password hash
from werkzeug.security import generate_password_hash, check_password_hash

# decorator
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'herecomesanyrandomsecretkey'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/Sporty'
mongo = PyMongo(app)



def login_required(f):
    @wraps(f)
    def wrapped_view(**kwargs):
        if session['logged_in'] is False:
            return redirect(url_for('getLogin'))

        return f(**kwargs)

    return wrapped_view


@app.get('/')
def index():
    return render_template('baseTemplate.html')


@app.post('/login')
def postLogin():
    req = request.form

    user_id = req['userid']
    pwd = req['password']

    resp = list(mongo.db.user.find({'userid': user_id}, {'_id':0, 'password':1}))
    if len(resp) < 1:
        flash('Incorrect User ID or Password!', 'danger')
        return redirect(url_for('getLogin'))
    else:
        check_ = check_password_hash(resp[0]['password'], pwd)

        if check_:
            session.clear()
            session['logged_in'] = True
            session['userid'] = user_id
            
            flash("Login successful", 'success')
            return redirect(url_for('HomePage'))
        else:
            flash('Incorrect Email or Password', 'danger')
            return redirect(url_for('getLogin'))


@app.get('/login')
def getLogin():
    return render_template('login.html')


@app.route('/logout')
def logout(): 
    session.clear()
    session['logged_in'] = False
    return render_template('baseTemplate.html')


@app.post('/signup')
def postSignup():
    req = request.form

    userid = req['userid']
    email = req['email']
    password = req['password']

    hashed_pw = generate_password_hash(password)

    mongo.db.user.insert_one(
        {
            'userid': userid,
            'email': email,
            'password': hashed_pw,
        }
    )

    return render_template('login.html')


@app.get('/signup')
def getSignup():
    return render_template('signup.html')


@app.route('/userhome')
@login_required
def HomePage():
    return render_template('home.html')



if __name__ == "__main__":
    app.run(debug=True)