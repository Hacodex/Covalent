# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template, redirect, session, url_for, request
from flask_pymongo import PyMongo
import bcrypt
import model
import os

# -- Initialization section --
app = Flask(__name__)
app.secret_key = "9AA6Ghg6je.EhDW3fe.34mkm4NJ"
user = os.environ['user']
pw = os.environ['pw']

# name of database
app.config['MONGO_DBNAME'] = 'MHacks2020'

#URI of database
app.config['MONGO_URI'] = f'mongodb+srv://{user}:{pw}@cluster0.6gvi8.mongodb.net/MHacks2020?retryWrites=true&w=majority'

mongo = PyMongo(app)

# -- Routes section --
# INDEX

@app.route('/')
@app.route('/index')

def index():
    return render_template('index.html', events = events)


# -- SIGN UP ROUTE
app.route('/signup', methods=['POST','GET'])
def signup():
    if request.method=='POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['email']})
        if existing_user is None: ## -- Checks to see if there is someone with this email inputted
            encrypred_pw = request.form['password']
    return render_template('signup.html')

# -- LOG IN ROUTE
@app.route('/login', methods=['POST', 'GET'])
def login():
    return(render_template('login.html'))


# -- LOG OUT ROUTE
@app.route('/logout')
def logout():
    return redirect('/')

@app.route('/add')
def add():
    # connect to the database

    # insert new data

    # return a message to the user
    return ""
