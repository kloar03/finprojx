from pprint import PrettyPrinter
from flask import render_template, flash, redirect, url_for, request, render_template_string
from datetime import date
from werkzeug.utils import html
from app import flask_app
from app.forms import (
    SimulateForm,
    ScheduleForm,
    AddEventForm,
    AddAccountForm,
    DropCollectionsForm
)
# simulation operations
from utils.scheduler import Scheduler
from utils.accounts import Savings, Loan
from utils.event import Event
from utils.time_utils import (
    generate_days,
    number_of_days_in_year,
)

# utility functions
from .route_funcs import add_event_main, add_account_main
from .tables import SavingsTable, LoansTable, EventsTable
# database operations
from mongoengine import connect
from db.nosql_account import NoSQL_Account


pp = PrettyPrinter(indent=2)

# some globals
mongo_client = connect('finprojx_app', host='localhost', port=27017)
db = mongo_client['finprojx']
event_arg_lists = []
# event_manager = Scheduler(2085)

accounts = {
    'AmeriCU': Savings('AmeriCU', 10000, .0025),
    'Mortgage_1': Loan('Mortgage_1', 178000, .03625, 30),
}
events = {
    'Mortgage_1_Pay': Event(credit_dict={accounts['AmeriCU']:811.77},
                           debit_dict={accounts['Mortgage_1']:811.77}),
    'Paycheck': Event(debit_dict={accounts['AmeriCU']:2600})
}

event_arg_lists = [
    ['Mortgage_1_Pay',events['Mortgage_1_Pay'], date(2021,6,14), 'every month'],
    ['Paycheck',events['Paycheck'], date(2021,6,19), 'every month'],
]

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
    event_dicts = []
    for name, event in events.items():
        event_dict = {}
        event_dict['name'] = name
        ca_names = [acct.name for acct in event.credit_dict]
        event_dict['credit_accounts'] = '\n'.join(ca_names)
        event_dict['credit_amounts'] = '\n'.join(map(str, event.credit_dict.values()))
        da_names = [acct.name for acct in event.debit_dict]
        event_dict['debit_accounts'] = '\n'.join(da_names)
        event_dict['debit_amounts'] = '\n'.join(map(str, event.debit_dict.values()))
        event_dicts.append(event_dict)
    events_table = EventsTable(event_dicts,
                               html_attrs={'style':"white-space:pre-wrap; word-wrap:break-word"}) 
    return render_template('home.html', title=title,
                           s_table=savings_table, l_table=loan_table,
                           e_table=events_table)

@flask_app.route('/add/event', methods=['GET','POST'])
def add_event():
    form = AddEventForm()
    # populate the choices w/ current accounts
    cur_accounts = list(accounts.keys())
    for entry in form.credit_accounts.entries:
        entry.account.choices = cur_accounts
    for entry in form.debit_accounts.entries:
        entry.account.choices = cur_accounts
    title = 'Add Event'
    if request.method == 'POST' and form.add_credit.data: # POST
        form.credit_accounts.append_entry()
        form.credit_accounts.entries[-1].account.choices = cur_accounts
        return render_template('add_event.html', title=title, form=form)
    elif request.method == 'POST' and form.add_debit.data:
        form.debit_accounts.append_entry()
        form.debit_accounts.entries[-1].account.choices = cur_accounts
    elif form.submit() and form.more.data: # an actual submission
        event = add_event_main(form, accounts)
        for name in event:
            events[name] = event[name]
        if event:
            return redirect(url_for('add_event'))
    elif form.submit() and form.submit.data: # an actual submission
        try:
            event = add_event_main(form, accounts)
            for name in event:
                events[name] = event[name]
        except:
            ...
        finally:
           return redirect('/')
        
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

@flask_app.route('/schedule', methods=['GET','POST'])
def schedule():
    title = 'Schedule Event'
    form = ScheduleForm()
    event_list = list(events.keys())
    form.event.choices = event_list
    if form.submit() and request.method == 'POST':
        name = form.event.data
        event = events[name]
        start = form.start_date.data
        freq = form.frequency.data
        units = form.frequency_units.data
        # event_manager.add_event(name, event, start, f'{freq} {units}')
        event_arg_lists.append(
            [name, event, start, f'{freq} {units}']
        )
    return render_template('schedule.html', title=title, form=form)

@flask_app.route('/simulate', methods=['GET','POST'])
def simulate():
    title = 'Simulate'
    form = SimulateForm()
    if form.submit() and request.method == 'POST':
        seq_name = 'original'
        cur_year = date.today().year
        num_years = form.sim_years.data
        fin_year = cur_year + num_years
        event_manager = Scheduler(fin_year)
        for event_args in event_arg_lists:
            event_manager.add_event(*event_args)
        docs = []
        for year in range(cur_year, fin_year):
            num_days = number_of_days_in_year(year)
            for day in generate_days(year):
                for event in event_manager[day]:
                    event()
                for account in accounts.values():
                    account.apply_interest(interest_units='days',
                                            number_of_days=num_days)
                    try:
                        value = account.principle
                    except AttributeError:
                        value = account.amount

                    doc = NoSQL_Account(
                        sim_id=seq_name,
                        account_type=type(account).__name__,
                        account_name=account.name,
                        year=day.year,
                        month=day.month,
                        day=day.day,
                        value=value,
                        rate=account.rate
                    )
                    docs.append(doc)
            NoSQL_Account.objects.insert(docs)
            docs = []
        return redirect(url_for('view'))
    return render_template('simulate.html', title=title, form=form)

@flask_app.route('/data', methods=['GET'])
def data():
    title = 'Data Viewer'
    graph_data = []
    for account in accounts:
        acc_docs = NoSQL_Account.objects(account_name=account)
        trace = {
            'type': "scatter",
            'mode': "lines",
            'name': account,
            'x': [f'{doc.year}-{doc.month}-{doc.day}' for doc in acc_docs],
            'y': [doc.value for doc in acc_docs],
        }
        graph_data.append(trace)
    layout = {'title': 'Simulation X'}
    return render_template('data.html', title=title,
                           graph_data=graph_data, layout=layout)

@flask_app.route('/drop', methods=['GET', 'POST'])
def drop():
    title = 'Drop Form'
    form = DropCollectionsForm()
    if form.validate_on_submit(): # POST
        NoSQL_Account.drop_collection()
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
    html_string = "{% extends 'base.html' %}\n"

    html_string += "{% block app_content %}\n"
    html_string += '<h1>A temporary data viewer!</h1>'
    for doc in NoSQL_Account.objects[:10]:
        html_string += \
            f'<p>{doc.account_name}: {doc.value} on {doc.year}-{doc.month}-{doc.day}</p>'
    html_string += "{% endblock %}"
    return render_template_string(html_string)

@flask_app.route('/accounts', methods=['GET'])
def account_route():
    title = 'Account Viewer'
    html_string = '<html><h1>A temporary account viewer!</h1>'
    for name in accounts:
        html_string += \
            f'<p>{accounts[name]}</p>'
    html_string += '</html>'
    return html_string