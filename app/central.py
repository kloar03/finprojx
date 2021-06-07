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
