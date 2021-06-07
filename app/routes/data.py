from flask import render_template

from app import flask_app
from db.nosql_account import NoSQL_Account
from utils.accounts import Savings, Loan

accounts = {
    'AmeriCU': Savings('AmeriCU', 10000, .0025),
    'Mortgage_1': Loan('Mortgage_1', 178000, .03625, 30),
}

@flask_app.route('/data', methods=['GET'])
def data():
    title = 'Data Viewer'
    graph_data = []
    for account in accounts:
        acc_docs = NoSQL_Account.objects(account_name=account)
        trace = {
            'type': "scatter",
            'mode': "lines",
            'name': account,
            'x': [f'{doc.year}-{doc.month}-{doc.day}' for doc in acc_docs],
            'y': [doc.value for doc in acc_docs],
        }
        graph_data.append(trace)
    layout = {'title': 'Simulation X'}
    return render_template('data.html', title=title,
                           graph_data=graph_data, layout=layout)
