from bs4 import BeautifulSoup

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
    table = SavingsTable(accounts, html_attrs={'id':"savingsTable"})
    return add_edit_delete_to_table(table.__html__())

def build_loans_table():
    Config.MONGO[Config.DB]
    accounts = DB_Account.objects(type='Loan')
    table = LoansTable(accounts, html_attrs={'id':"loanTable"})
    return add_edit_delete_to_table(table.__html__())

def build_events_table():
    Config.MONGO[Config.DB]
    event_dicts = []
    for event in DB_Event.objects():
        event_dict = {}
        event_dict['name'] = event.name
        c_accs = [acc.name for acc in event.credit_accounts]
        event_dict['credit_accounts'] = '<br>'.join(c_accs)
        d_accs = [acc.name for acc in event.debit_accounts]
        event_dict['debit_accounts'] = '<br>'.join(d_accs)
        c_amts = [str(amt) for amt in event.credit_amounts]
        event_dict['credit_amounts'] = '<br>'.join(c_amts)
        d_amts = [str(amt) for amt in event.debit_amounts]
        event_dict['debit_amounts'] = '<br>'.join(d_amts)
        event_dicts.append(event_dict)
    table = EventsTable(event_dicts, html_attrs={'id': 'eventTable'})
    return add_edit_delete_to_table(table.__html__())

def add_edit_delete_to_table(html_table: str):
    """ adds edit and delete buttons to every row """
    soup = BeautifulSoup(html_table, 'html.parser')
    # print(soup.prettify())
    body = soup.find('tbody')
    rows = body.find_all('tr')
    edit_string = \
        '<div class="left-icon-container">\n' +\
        '\t<span class="edit-icon glyphicon glyphicon-pencil"></span>' +\
        '</div>\n'
    delete_string = \
        '<div class="right-icon-container">\n' +\
        '\t<span class="delete-icon glyphicon glyphicon-trash"></span>' +\
        '</div>\n'

    for row in rows:
        first, *_, last = row.find_all('td')
        # TODO: handle empty last cell (event table)
        try: first.string = '\n'.join([edit_string, first.string])
        except TypeError: ...
        try: last.string = '\n'.join([delete_string, last.string])
        except TypeError: ...
    return soup.prettify(formatter=None)