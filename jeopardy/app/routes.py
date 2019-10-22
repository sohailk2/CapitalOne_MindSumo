from flask import render_template, flash, redirect, url_for, request
from app import app
import json
import requests


# https://www.dataquest.io/blog/python-api-tutorial/ THIS IS HOW TO GET THE JSON CONTENT AND STUFF


#so to do this once load ur json stuff here

categoryList = None
with open('app/data/categoryListOne') as json_file:
    categoryList = json.load(json_file)

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'JACK'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/viewQuestions')
def viewQuestions():

    # can add a loading screen before this stuff in html from home page to make it look cool
    
    category = request.args.get('category')
    page = request.args.get('page')

    # so what this page is going to do is just display the results and stuff
    # those elements should have the option to add to saved questions and stuff

    # first see what the id of the related category is
    categoryIds = None
    if (category != None):
        categoryIds = list(filter(lambda question: question['title']!= None and category in question['title'], categoryList))

    # now use the jservice to get the questions with those specifications every thing in here
    query = []


    for categoryId in categoryIds:
        query = query + requests.get("http://jservice.io/api/clues?category={}".format(categoryId['id'])).json()
        
    return render_template('viewQuestions.html', title='Search Questons', results = query)