from flask import render_template
from app import flask_app

@flask_app.route('/')
@flask_app.route('/home')
def home():
    title = 'Home'
    return render_template('home.html', title=title)

@flask_app.route('/add')
def add():
    return render_template('add.html')