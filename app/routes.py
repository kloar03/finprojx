from flask import render_template, flash, redirect, url_for, request
from app import flask_app
from app.forms import AddEventForm

@flask_app.route('/')
@flask_app.route('/home')
def home():
    title = 'Home'
    return render_template('home.html', title=title)

@flask_app.route('/add-event', methods=['GET','POST'])
def add_event():
    form = AddEventForm()
    title = 'Add Event'
    if form.validate_on_submit(): # POST
        flash(f"Date:{form.date.data}, Frequency:{form.frequency.data}")
        return redirect(url_for('home'))
    elif request.method:
        flash(form.errors)
    return render_template('add_event.html', title=title, form=form)

@flask_app.route('/data', methods=['GET'])
def data():
    title = 'Data Viewer'
    return render_template('data.html', title=title)