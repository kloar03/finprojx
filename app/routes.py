from flask import render_template, flash, redirect, url_for, request
from app import flask_app
from app.forms import (
    AddEventForm,
    AddAccountForm,
    DropCollectionsForm
)
# simulation operations
from utils.scheduler import Scheduler
from utils.accounts import Savings, Loan
from utils.event import Event

# utility functions
from .route_funcs import add_event_main, add_account_main
from .tables import SavingsTable, LoansTable
# database operations
from mongoengine import connect
from db.nosql_account import NoSQL_Account

# some globals
mongo_client = connect('finprojx_app', host='localhost', port=27017)
db = mongo_client['finprojx']
event_manager = Scheduler(2085)


accounts = {
    'AmeriCU': Savings('AmeriCU', 10000, .025),
    'Mortgage_1': Loan('Mortgage_1', 178000, 3.65, 30),
}

@flask_app.route('/')
@flask_app.route('/home')
def home():
    title = 'Home'
    savings_accts = [accounts[n] for n in accounts
                     if isinstance(accounts[n], Savings)]
    loan_accts = [accounts[n] for n in accounts
                     if isinstance(accounts[n], Loan)]
    savings_table = SavingsTable(savings_accts,
                                 html_attrs={'style':"float: left;"})
    loan_table = LoansTable(loan_accts,
                            html_attrs={'style':"float: right;"})
    return render_template('home.html', title=title,
                           s_table=savings_table, l_table=loan_table)

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
        account = add_account_main(form)
        for name in account:
            accounts[name] = account[name]    
        if account:
            red_to = '/' if form.data['submit'] else url_for('add_account')
            return redirect(red_to)
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

@flask_app.route('/accounts', methods=['GET'])
def account_route():
    title = 'Account Viewer'
    html_string = '<html><h1>A temporary account viewer!</h1>'
    for name in accounts:
        html_string += \
            f'<p>{accounts[name]}</p>'
    html_string += '</html>'
    return html_string