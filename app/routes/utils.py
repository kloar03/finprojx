from app import Config

from app.tables import (
    SavingsTable,
    LoansTable,
    EventsTable,
)
from db import (
    DB_Account,
    DB_Event,
)

def build_savings_table():
    Config.MONGO[Config.DB]
    accounts = DB_Account.objects(type='Savings')
    return SavingsTable(accounts, html_attrs={'id':"savingsTable"})

def build_loans_table():
    Config.MONGO[Config.DB]
    accounts = DB_Account.objects(type='Loan')
    return LoansTable(accounts, html_attrs={'id':"loanTable"})

def build_events_table():
    Config.MONGO[Config.DB]
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
    return EventsTable(event_dicts,
                       html_attrs={'id': 'eventTable',
                           'style':"white-space:pre-wrap; word-wrap:break-word;"})