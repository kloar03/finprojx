from datetime import date
from flask import (
    redirect,
    render_template,
    request,
    url_for,
)

from app import flask_app, Config
from app.forms import SimulateForm
from db import (
    DB_Account,
    DB_Event,
    DB_Scheduler,
    DB_Simulate
)
from utils import accounts
from utils.accounts import Savings, Loan
from utils.event import Event
from utils.scheduler import Scheduler
from utils.time_utils import (
    generate_days,
    number_of_days_in_year,
)

@flask_app.route('/simulate', methods=['GET','POST'])
def simulate():
    Config.MONGO[Config.DB]
    title = 'Simulate'
    form = SimulateForm()
    if form.submit() and request.method == 'POST':
        seq_name = 'original'
        cur_year = date.today().year
        num_years = form.sim_years.data
        fin_year = cur_year + num_years
        event_manager = Scheduler(fin_year)
        accounts, events = build_objects()
        fill_scheduler(event_manager, events)
        docs = []
        for year in range(cur_year, fin_year):
            num_days = number_of_days_in_year(year)
            for day in generate_days(year):
                for event in event_manager[day]:
                    event()
                for account in accounts.values():
                    amount = account.apply_interest(interest_units='days',
                                                    number_of_days=num_days)
                    doc = DB_Simulate(
                        name=seq_name,
                        account=DB_Account.objects(name=account.name)[0],
                        date=day,
                        amount=amount
                    )
                    docs.append(doc)
            DB_Simulate.objects.insert(docs)
            docs = []
        return redirect(url_for('data'))
    return render_template('simulate.html', title=title, form=form)

def build_objects():
    """ convenience for building objects from DB storage """
    # get the account objects
    accounts = {}
    for acct in DB_Account.objects():
        if acct.type == 'Savings':
            account = Savings(acct.name, amount=acct.value, rate=acct.rate)
        elif acct.type == 'Loan':
            account = Loan(acct.name, principle=acct.value, rate=acct.rate,
                           length=acct.length)            
        else:
            raise ValueError
        accounts[acct.name] = account
    # get the event objects
    events = {}
    for evt in DB_Event.objects():
        c_accts = [accounts[acct.name] for acct in evt.credit_accounts]
        c_amts = evt.credit_amounts
        d_accts = [accounts[acct.name] for acct in evt.debit_accounts]
        d_amts = evt.debit_amounts
        c_dict = dict(zip(c_accts, c_amts)) if c_accts else {}
        d_dict = dict(zip(d_accts, d_amts)) if d_accts else {}
        event = Event(credit_dict=c_dict,
                      debit_dict=d_dict)
        events[evt.name] = event
    return accounts, events

def fill_scheduler(scheduler, events):
    """ convenience function for readability """
    # get the event schedules
    for event_sched in DB_Scheduler.objects():
        name = event_sched.event.name
        event = events[name]
        scheduler.add_event(name, event, event_sched.start, 
                            f"{event_sched.freq} {event_sched.units}")
