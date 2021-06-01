from flask import render_template, flash, redirect, url_for, request
from app import flask_app
from app.forms import (
    AddEventForm,
    AddAccountForm,
    DropCollectionsForm
)
# simulation operations
from utils.scheduler import Scheduler
from utils.event import Event

# database operations
from mongoengine import connect
from db.nosql_account import NoSQL_Account

mongo_client = connect('finprojx_app', host='localhost', port=27017)
db = mongo_client['finprojx']
event_manager = Scheduler(2085)
@flask_app.route('/')
@flask_app.route('/home')
def home():
    title = 'Home'
    return render_template('home.html', title=title)

@flask_app.route('/add/event', methods=['GET','POST'])
def add_event():
    form = AddEventForm()
    title = 'Add Event'
    if form.validate_on_submit(): # POST
        flash(f"Date:{form.date.data}, Frequency:{form.frequency.data}")
    elif request.method:
        flash(form.errors)
    return render_template('add_event.html', title=title, form=form)

@flask_app.route('/add/account', methods=['GET','POST'])
def add_account():
    form = AddAccountForm()
    title = 'Add Account'
    if form.submit() and request.method == 'POST':
        if form.data['account_type'] == 'savings':
            flash('Savings!')
            if not form.data['rate']:
                flash('Enter a rate as a percentile (between 0-100)', category='error')
        elif form.data['account_type'] == 'loan':
            flash('Loan!')
        else:
            flash('Please select an account type!', category='error')
    
    return render_template('add_account.html', title=title, form=form)

@flask_app.route('/data', methods=['GET'])
def data():
    title = 'Data Viewer'
    return render_template('data.html', title=title)

@flask_app.route('/drop', methods=['GET', 'POST'])
def drop():
    title = 'Drop Form'
    form = DropCollectionsForm()
    if form.validate_on_submit(): # POST
        db.drop_collection('finprojx_app')
        flash('Collection Dropped')
    return render_template('drop.html', title=title, form=form)

@flask_app.route('/add', methods=['GET'])
def add():
    title = 'Add'
    return render_template('add.html', title=title)

@flask_app.route('/view', methods=['GET'])
def view():
    title = 'Data Viewer'
    html_string = '<html><h1>A temporary data viewer!</h1>'
    for doc in NoSQL_Account.objects[:10]:
        html_string += \
            f'<p>{doc}</p>'
    html_string += '</html>'
    return html_string