from datetime import date
from flask import (
    redirect,
    render_template,
    request,
    url_for,
)

from .add_account import add_account_main
from .add_event import (
    add_event_main,
    set_account_choices,
)
from app import flask_app, Config
from app.forms import (
    AddAccountForm,
    AddEventForm
)
from app.tables import (
    EventsTable,
    LoansTable,
    SavingsTable,
)
from db import (
    DB_Account,
    DB_Event,
)

@flask_app.route('/', methods=['GET', 'POST'])
@flask_app.route('/home', methods=['GET','POST'])
def home():
    title = 'Home'
    Config.MONGO[Config.DB]
    account_form = AddAccountForm()
    event_form = AddEventForm()
    set_account_choices(event_form.credit_accounts)
    set_account_choices(event_form.debit_accounts)
    
    savings_accts = DB_Account.objects(type='Savings')
    loan_accts = DB_Account.objects(type='Loan')
    savings_table = SavingsTable(savings_accts,
                                 html_attrs={'id':"savingsTable"})
    loan_table = LoansTable(loan_accts,
                            html_attrs={'id':"loanTable"})
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
                               html_attrs={'style':"white-space:pre-wrap; word-wrap:break-word;"}) 
    if account_form.submit() and request.method == 'POST':
        if add_account_main(account_form):
            redirect(url_for('home'))
    if event_form.submit() and request.method == 'POST':
        if add_event_main(event_form):
            redirect(url_for('home'))
    return render_template('home.html', title=title,
                           s_table=savings_table, l_table=loan_table,
                           e_table=events_table, account_form=account_form,
                           event_form=event_form)
