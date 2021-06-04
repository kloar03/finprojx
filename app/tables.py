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