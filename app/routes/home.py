from datetime import date
from db.DB_Event import DB_Event
from flask import render_template

from app import flask_app, Config
from app.tables import (
    EventsTable,
    LoansTable,
    SavingsTable,
)
from db import (
    DB_Account,
    DB_Event,
)

@flask_app.route('/')
@flask_app.route('/home')
def home():
    title = 'Home'
    Config.MONGO[Config.DB]
    savings_accts = DB_Account.objects(type='Savings')
    loan_accts = DB_Account.objects(type='Loan')
    savings_table = SavingsTable(savings_accts,
                                 html_attrs={'style':"float: left;"})
    loan_table = LoansTable(loan_accts,
                            html_attrs={'style':"float: right;"})
    event_dicts = []
    for event in DB_Event.objects():
        event_dict = {}
        event_dict['name'] = event.name
        c_accs = [acc.name for acc in event.credit_accounts]
        event_dict['credit_accounts'] = '\n'.join(c_accs)
        d_accs = [acc.name for acc in event.debit_accounts]
        event_dict['debit_accounts'] = '\n'.join(d_accs)
        c_amts = [str(amt) for amt in event.credit_amounts]
        event_dict['credit_amounts'] = '\n'.join(c_amts)
        d_amts = [str(amt) for amt in event.debit_amounts]
        event_dict['debit_amounts'] = '\n'.join(d_amts)
        event_dicts.append(event_dict)
    events_table = EventsTable(event_dicts,
                               html_attrs={'style':"white-space:pre-wrap; word-wrap:break-word"}) 
    return render_template('home.html', title=title,
                           s_table=savings_table, l_table=loan_table,
                           e_table=events_table)
