from flask_table import Table, Col

class SavingsTable(Table):
    no_items = 'No Savings Accounts Created'
    classes = ['table-striped', 'table-bordered', 'table-condensed']
    id = Col('ID', show=False)
    name = Col('Account Name')
    rate = Col('Annual Percent Yield')

class LoansTable(Table):
    no_items = 'No Loan Accounts Created'
    classes = ['table-striped', 'table-bordered', 'table-condensed']
    id = Col('ID', show=False)
    name = Col('Account Name')
    origination = Col('Origination Amount')
    rate = Col('Annual Percent Rate')

class EventsTable(Table):
    no_items = 'No Events Created Yet!'
    classes = ['table-striped', 'table-bordered', 'table-condensed']
    id = Col('ID', show=False)
    name = Col('Event Name')
    credit_accounts = Col('Credit Accounts')
    credit_amounts = Col('Credit Amounts')
    debit_accounts = Col('Debit Accounts')
    debit_amounts = Col('Debit Amounts')
    