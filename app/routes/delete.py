from flask import (
    Response
)

from app import flask_app, Config
from db import (
    DB_Account,
    DB_Event,
)

@flask_app.route('/delete/savings/<name>', methods=['GET'])
@flask_app.route('/delete/loan/<name>', methods=['GET'])
def delete_account(name):
    Config.MONGO[Config.DB]
    account = DB_Account.objects(name=name).delete()
    return Response(b'success', status=200)

@flask_app.route('/delete/event/<name>', methods=['GET'])
def delete_event(name):
    Config.MONGO[Config.DB]
    event = DB_Event.objects(name=name).delete()
    return Response(b'success', status=200)
