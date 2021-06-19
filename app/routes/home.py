from datetime import date
from flask import (
    jsonify,
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
from .utils import (
    build_savings_table,
    build_loans_table,
    build_events_table,
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

@flask_app.route('/', methods=['GET'])
@flask_app.route('/home', methods=['GET'])
def home():
    title = 'Home'
    Config.MONGO[Config.DB]
    account_form = AddAccountForm()
    event_form = AddEventForm()
    set_account_choices(event_form.credit_accounts)
    set_account_choices(event_form.debit_accounts)

    savings_table = build_savings_table()
    loans_table = build_loans_table()
    events_table = build_events_table()

    return render_template('home.html', title=title,
                           s_table=savings_table, l_table=loans_table,
                           e_table=events_table, account_form=account_form,
                           event_form=event_form)
