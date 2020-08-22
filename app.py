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
        jamesChu = {"name": "James Chu", "contact": "jameschu@umich.edu", "role": "Front and Backend Developer", "description": "I am an incoming freshman at the University of Michigan and I plan on studying computer science and business. Over quarantine, I've been drinking a lot of oat milk and I have a black lab named Parker. I hope to one day work in the FinTech industry."}
    winsonChen = {"name": "Winson Chen", "contact": "winsonc@umich.edu", "role": "Front and Backend Developer", "description": "I am a student who is interested in computer engineering. I spend my weekends playing games, reading books, and listening to music on Spotify. Fluent in English, Chinese (kind of), and Pokémon type match-ups"}
    aaronZheng = {"name": "Aaron Zheng", "contact": "aaronzg@umich.edu", "role": "Front and Backend Developer", "description": "I like playing basketball. I am going to major in computer science. I want to become an entrepreneur. I like problem solving. My dream job is to work at Google."}
    winstonCai = {"name": "Winston Cai", "contact": "", "role": "Supporting cast", "description": "Winston Cai is a high school graduate from the Bronx High School of Science. I am interested in the humanities."}
    devTeam = [jamesChu, winsonChen, aaronZheng, winstonCai]
    devPictures = ["https://www.bxsml.org/images/james.png", "https://media-exp1.licdn.com/dms/image/C4E03AQEZfz3_MHQOPg/profile-displayphoto-shrink_800_800/0?e=1603324800&v=beta&t=-d1pAMh1b1o998JAkwRIObB_iJl6sQZajKSWQKvBTg8", "https://media-exp1.licdn.com/dms/image/C4D03AQEmAsrlxua3lA/profile-displayphoto-shrink_800_800/0?e=1603324800&v=beta&t=k1lxF4VfyTvl75WpUGvo2UiqC4QljZ3Uzw_ORRelV0s", "https://media-exp1.licdn.com/dms/image/C4D03AQENNgwoEmNeyA/profile-displayphoto-shrink_200_200/0?e=1603324800&v=beta&t=KdBQfIBaZ0zMX6hzdFLj51LJAlQM946BiPtgQHXINgo"]
    loggedIn = session
    return render_template('index.html', **locals())


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
    info = mongo.db.info
    users = mongo.db.users
    basic = users.find_one({'username' : username})
    if basic:
        user_info = info.find_one({'email' : basic['email']})
        return render_template('user.html', basic=basic, user_info=user_info)
    return "Sorry, no profile. <a href='/index'>Return to welcome page</a>"

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
