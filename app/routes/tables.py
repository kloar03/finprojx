from flask import jsonify

from .utils import (
    build_savings_table,
    build_loans_table,
    build_events_table,
)
from app import flask_app, Config
from app.tables import (
    SavingsTable,
    LoansTable,
    EventsTable,
)
from db import DB_Account

@flask_app.route('/tables/savings', methods=['GET'])
def getSavingsTable():
    table = build_savings_table()
    return jsonify(table)

@flask_app.route('/tables/loan', methods=['GET'])
def getLoansTable():
    table = build_loans_table()
    return jsonify(table)

@flask_app.route('/tables/event', methods=['GET'])
def getEventsTable():
    table = build_events_table()
    return jsonify(table)
