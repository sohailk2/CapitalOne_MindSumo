from flask import render_template, flash, redirect, url_for
from app import app

# https://www.dataquest.io/blog/python-api-tutorial/ THIS IS HOW TO GET THE JSON CONTENT AND STUFF

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
    return render_template('viewQuestions.html', title='Home')