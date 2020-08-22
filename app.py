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
            encrypted_pw = request.form['password']
            users.insert({'email' : request.form['email'], 'password' : encrypted_pw, "name" : request.form['fullname'], 'username' : request.form['username'], 'phone' : request.form['phone']}) # Adds info to database
            session['email'] = request.form['email']
            return redirect(url_for('survey'))
        return('That email is already linked to another account! Try logging in!')
    return render_template('signup.html')

# -- LOG IN ROUTE
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        users = mongo.db.users
        login_user = users.find_one({'email' : request.form['email']})
        if login_user:
            if(bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user["password"].encode('utf-8')): 
                session['email'] = request.form['email']
                return redirect(url_for('index'))
        return 'Invalid email/password combination :/'
    return(render_template('login.html'))


# -- LOG OUT ROUTE
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# -- SURVEY ROUTE 
@app.route('/survey', methods=['POST','GET'])
def survey():
    if request.method=='POST': 
        if not session:
            return redirect('/')
        info = mongo.db.info 
        scores = mongo.db
        info.insert({'email' : session['email'], 'description' : request.form['description'], 'state' : request.form['state'], 'city' : request.form['city'], 'school' : request.form['school'], 'classes' : request.form['classes']})
        return redirect(url_for('index'))
    return render_template('survey.html')

@app.route('/user/<username>')
def user(username):
    return(render_template('user.html'))

@app.route('/connect')
def connect():
    usersDB = mongo.db.users.find({})
    infoDB = mongo.db.info.find({})
    allUserData = []
    for user in usersDB:
        allUserData.append(user)
    for i in range(len(tmp[i])):
        allUserData[i].update(tmp[i])
    return render_template('connect.html', **locals)

@app.route('/add')
def add():
    # connect to the database
    users = mongo.db.users
    # insert new data
    users.insert({"hi":"HELLO"})
    # return a message to the user
    return "Connection succesfful!"
