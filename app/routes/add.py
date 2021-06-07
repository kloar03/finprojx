from flask import render_template

from app import flask_app

@flask_app.route('/add', methods=['GET'])
def add():
    title = 'Add'
    return render_template('add.html', title=title)
