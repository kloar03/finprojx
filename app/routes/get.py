from flask import (
    jsonify,
    Response
)

from app import flask_app, Config
from db import (
    DB_Account,
    DB_Event,
)


@flask_app.route('/get/savings/<name>', methods=['GET'])
@flask_app.route('/get/loan/<name>', methods=['GET'])
def get_account(name):
    Config.MONGO[Config.DB]
    account = DB_Account.objects(name=name)[0].to_json()
    return jsonify(account)

@flask_app.route('/get/event/<name>', methods=['GET'])
def get_event(name):
    Config.MONGO[Config.DB]
    event = DB_Event.objects(name=name)[0].to_json()
    return jsonify(event)