# ---- YOUR APP STARTS HERE ----
# -- Import section --
from flask import Flask
from flask import render_template, redirect, session, url_for, request
from flask_pymongo import PyMongo
import bcrypt
import model
import os
import requests
import timeit
import csv
import datetime

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

# -- LOG IN AND SIGN UP TOGETHER ROUTE 
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        users = mongo.db.users
        info = mongo.db.info
        login_user = users.find_one({'email' : request.form['email']})
        if login_user:
            if(bcrypt.hashpw(request.form['password'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user["password"].encode('utf-8')): 
                session['email'] = request.form['email']
                return redirect(url_for('index'))
        if len(request.form) != 5:
            return 'Invalid email/password combination 😕'
        if login_user is None: # -- Checks to see if there is already someone with the email inputted
            encrypted_pw = str(bcrypt.hashpw(request.form['password'].encode("utf-8"), bcrypt.gensalt()), 'utf-8') #Encrypts password using bcrypt
            users.insert({'email' : request.form['email'], 'password' : encrypted_pw, 'name' : request.form['fullname'], 'username' : request.form['username'], 'phone' : request.form['phone']}) # Inserts data into mongodb database in format of a dictionary
            session['email'] = request.form['email'] # Sets session cookie to email so user is logged in
            return redirect(url_for('survey')) # Sends user to index page
        return('That email is already associated with another account. Try logging in!') # Since user already has email this message is shown
    return(render_template('login.html'))


# -- LOG OUT ROUTE
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# -- SURVEY ROUTE 
@app.route('/survey', methods=['POST','GET'])
def survey():
    start = timeit.default_timer()
    if request.method=='POST':
        if not session:
            return redirect('/')
        info = mongo.db.info
        scores = mongo.db.scores
        inputDict = {'email' : session['email'], 'description' : request.form['description'], 'state' : request.form['state'], 'city' : request.form['city'], 'school' : request.form['school'], 'classes' : request.form['classes']}
        info.insert(inputDict)
        
        ##Load Embeddings Once To Reduce Runtime
        with open('./csv/Word_List.csv', newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            print(reader)
            wordList = list(reader)
            wordList = [elem[0] for elem in wordList]
            del wordList[0]
        with open('./csv/GloVe_Embeddings_1.csv', newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            tmp1 = list(reader)
            del tmp1[0]
        with open('./csv/GloVe_Embeddings_2.csv', newline='', encoding="utf-8") as f:
            reader = csv.reader(f)
            tmp2 = list(reader)
            del tmp2[0]
        embeddings = tmp1 + tmp2
        currUser, userModel = model.Results.makeAll(inputDict, wordList, embeddings)
        keys = ["email"] + ["openness", "conscientiousness", "neuroticism", "extraversion", "agreeableness"]
        userScores = [session["email"]] + userModel.finalscores
        scoresDict = dict(zip(keys, userScores))
        scores.insert(scoresDict)
        end = timeit.default_timer()
        print("Runtime:", end-start)
        return redirect(url_for('index'))
    return render_template('survey.html')

@app.route('/user/<username>')
def user(username):
    info = mongo.db.info
    users = mongo.db.users
    mongo_posts = mongo.db.posts.find({})
    basic = users.find_one({'username' : username})
    if basic:
        user_info = info.find_one({'email' : basic['email']})
        posts = []
        for post in mongo_posts:
            posts.append(post)
        timeline = []
        for post in posts: 
            if post['recipient'] == basic['username']:
                timeline.append(post)
        print(timeline) 
        return render_template('user.html', basic=basic, user_info=user_info, timeline=timeline)
    return "Sorry, no profile. <a href='/index'>Return to welcome page</a>"

@app.route('/connect')
def connect():
    #info = mongo.db.info
    #users = mongo.db.users
    usersDB = mongo.db.users.find({})
    infoDB = mongo.db.info.find({})
    scoresDB = mongo.db.scores.find({})
    users = []
    for user in usersDB:
        users.append(user)
    
    info = []
    for user in infoDB:
        info.append(user)

    if model.Results.getIndexOfUser(session["email"], info) == "You are dumb":
        return redirect(url_for('survey'))
    
    scores = []
    for user in scoresDB:
        scores.append(user)

    res = model.Results(session["email"], users, info, scores)
    teamMembers, friendsLocation, friendsSchool, friendsClasses = res.main()
    return render_template('connect.html', **locals())

@app.route('/createPost', methods=['POST','GET'])
def createPost():
    if request.method=="POST": 
        if session:
            usersDB = mongo.db.users.find({})
            infoDB = mongo.db.info.find({})
            scores = mongo.db.scores
            posts = mongo.db.posts
            basic = mongo.db.users.find_one({'username' : request.form['username']})
            loggedInUser = mongo.db.users.find_one({'email' : session['email']})
            if basic:
                now = datetime.datetime.now()
                timeStamp = now.strftime("%Y-%m-%d %H:%M:%S")
                posts.insert({"author":loggedInUser['name'],"authorUsername":loggedInUser['username'], "recipient":request.form['username'], "time":timeStamp, "title":request.form["title"], "post":request.form["post"]})
                return redirect(url_for('index'))
        return "You are not logged in. Please <a href='login'>log in or sign up</a>"
    return render_template('createPost.html')

@app.route('/add')
def add():
    # connect to the database
    users = mongo.db.users
    # insert new data
    users.insert({"hi":"HELLO"})
    # return a message to the user
    return "Connection succesfful!"
