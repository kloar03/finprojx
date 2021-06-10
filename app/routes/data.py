from flask import render_template

from app import flask_app
from db import (
    DB_Account,
    DB_Simulate,
)
from utils.accounts import Savings, Loan

@flask_app.route('/data', methods=['GET'])
def data():
    title = 'Data Viewer'
    graph_data = []
    for account in DB_Account.objects():
        acc_docs = DB_Simulate.objects(account=account)
        trace = {
            'type': "scatter",
            'mode': "lines",
            'name': account.name,
            'x': [f'{doc.date}' for doc in acc_docs],
            'y': [doc.amount for doc in acc_docs],
        }
        graph_data.append(trace)
    layout = {'title': 'Simulation X'}
    return render_template('data.html', title=title,
                           graph_data=graph_data, layout=layout)
