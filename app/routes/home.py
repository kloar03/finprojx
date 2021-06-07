from datetime import date
from flask import render_template

from app import flask_app
from app.tables import (
    EventsTable,
    LoansTable,
    SavingsTable,
)
from utils.accounts import (
    Savings,
    Loan,
)
from utils.event import Event

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
