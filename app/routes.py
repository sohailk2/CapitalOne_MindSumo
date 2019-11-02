from flask import render_template, flash, redirect, url_for, request
from app import app
import json
import requests
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app.models import User, Question
from app import db
import ast
import random
import datetime




# https://www.dataquest.io/blog/python-api-tutorial/ THIS IS HOW TO GET THE JSON CONTENT AND STUFF


#so to do this once load ur json stuff here

categoryList = None
with open('app/data/categoryListOne') as json_file:
    categoryList = json.load(json_file)

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))


    if request.method == 'POST':

        if request.form.get('formName') == "Login":
            print(request.form.get('username'))
            
            user = User.query.filter_by(username=request.form.get('username')).first()

            if user is None or not user.check_password(request.form.get('password')):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user)
            return redirect(url_for('home'))

        if request.form.get('formName') == "Register":
             # first check if the name is valid
            user = User.query.filter_by(username=request.form.get('username')).first()
            if user is not None:
                flash('User Name Already Exists. Register with different username.')
                return redirect(url_for('login'))
            
            # else then make the account
            user = User(username=request.form.get('username'))
            user.set_password(request.form.get('password'))
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, {} is now a registered user!'.format(request.form.get('username')))
            return redirect(url_for('login'))
    
    
    return render_template('login.html', title='Sign In')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/search', methods = ['GET', 'POST'])
@login_required
def search():

    if request.method == 'POST':
        category = request.form.get('category')
        points = request.form.get('pointValue')

        datetimes = request.form.get('datetimes')
        print(request.form)

        if datetimes != None:
            # parse out the dates
            # get proper format
            # and then pass in to query
            date1 = (datetimes.split(' - '))[0]
            date1 = datetime.datetime.strptime(date1, '%m/%d/%Y')

            date2 = (datetimes.split(' - '))[0]
            date2 = datetime.datetime.strptime(date2, '%m/%d/%Y')
            return redirect(url_for('viewQuestions', category = category, value=points,  mindate=date2, maxdate=date1))
            


        return redirect(url_for('viewQuestions', category = category, value=points))


    return render_template('search.html', title='Search')

@app.route('/jeopardySetup', methods = ['GET', 'POST'])
@login_required
def jeopardySetup():

    if request.method == 'POST':
        # get the type random or not
        gameGenType = request.form.get('boardType')

        if (gameGenType == 'generate'):
            return url_for(jeopardy, categories = request.form.get('data'))

    return render_template('jeopardySetup.html', title='Setup Game')

@app.route('/jeopardy', methods = ['GET', 'POST'])
@login_required
def jeopardy():

    categories = json.loads(request.args.get('categories'))

    gameData = []

    # so for each of these categories return a question
    if categories != None:
        for category in categories:
            newData = getQuestionSet(category)
            if not (len(newData) < 5):
                gameData.append(newData)

    print(gameData[0][0]['answer'])


    return render_template('jeopardy.html', title='Setup Game', gameData = gameData)

def getQuestionSet(category):
    # first i need to get the id of this question from cat list
    questionId = list(filter(lambda question: question['title']!= None and category.lower() in question['title'].lower(), categoryList))
    if (len(questionId) == 0):
        return []
    else:
        questionSet = questionId[0] # just get the first one 
        # now get the question data using jservice api
        apiQuery = "http://jservice.io/api/clues?category={}".format(questionSet['id'])
        result = requests.get(apiQuery).json()

        return generateQuestions(result)


def generateQuestions(questionData):
    
    outputData = []

    valueList = [200, 400, 600, 800, 1000]

    for value in valueList:
        questions = list(filter(lambda question: question['value'] != None and question['value'] == value, questionData))
        if (len(questions) != 0):
            outputData.append(random.choice(questions))

    return outputData



@app.route('/home')
@login_required
def home():
    return render_template('home.html', title='Home')

@app.route('/viewFavorites', methods = ['GET', 'POST'])
@login_required
def viewFavorites():

    favorites = Question.query.filter_by(user_id=current_user.id).all()

    # for each one of these things in here i need to convert to json
    for i in range(0, len(favorites)):
        favorites[i] = ast.literal_eval(favorites[i].data)

    return render_template('viewFavorites.html', title="Favorites", results = favorites)

@app.route('/viewQuestions', methods = ['GET', 'POST'])
@login_required
def viewQuestions():

    if request.method == 'POST':
        # first check if this is already in favorites

        questionQuery = Question.query.filter_by(data=request.form.get('data')).all()
        print(questionQuery)
        if (len(questionQuery) == 0):
            # add to the database
            q = Question(data=request.form.get('data'), author=current_user)
            db.session.add(q)
            db.session.commit()
            # print added to favorites
            print("ADDED TO FAVORITES")

        # return redirect(url_for('home'))


    # can add a loading screen before this stuff in html from home page to make it look cool
    
    category = request.args.get('category')
    page = request.args.get('page')
    value = request.args.get('value')
    maxdate = request.args.get('maxdate')
    mindate = request.args.get('mindate')


    # so what this page is going to do is just display the results and stuff
    # those elements should have the option to add to saved questions and stuff

    # first see what the id of the related category is
    categoryIds = None
    if (category != None):
        categoryIds = list(filter(lambda question: question['title']!= None and category.lower() in question['title'].lower(), categoryList))

    # now use the jservice to get the questions with those specifications every thing in here
    query = []

    # paginaton
    if (page == None):
        page = 0
    else:
        page = int(page)

    if (value == None):
        value = 0
    else:
        value = int(value)

    if (maxdate == None):
        maxdate = ""
    
    if (mindate == None):
        mindate = ""

    
    
    if (page > len(categoryIds) - 1):
        query = []
    else:
        apiQuery = "http://jservice.io/api/clues?category={}".format(categoryIds[page]['id'])

        if value != 0:
            apiQuery += "&value={}".format(value)


        apiQuery += "&min_date={}".format(mindate)
        apiQuery += "&max_date={}".format(maxdate)

        print("API QUERY" + apiQuery)

        result = requests.get(apiQuery).json()
        
        # do stuff to the results here
        # removing nulls and stuff
        # format date?
        query = query + result


    
    return render_template('viewQuestions.html', title='Search Questons', results = query, pages = len(categoryIds), currentPage = page)