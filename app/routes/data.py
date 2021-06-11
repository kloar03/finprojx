from flask import render_template
from numpy import argsort, array

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
        dates = array([doc.date for doc in acc_docs])
        amounts = array([doc.amount for doc in acc_docs])
        sort_idxs = argsort(dates)
        dates = [f"{d}" for d in dates[sort_idxs]]
        trace = {
            'type': "scatter",
            'mode': "lines",
            'name': account.name,
            'x': dates,
            'y': amounts[sort_idxs].tolist(),
        }
        graph_data.append(trace)
    layout = {'title': 'Simulation X'}
    return render_template('data.html', title=title,
                           graph_data=graph_data, layout=layout)
