from flask import (
    request,
    jsonify,
    Response,
)
from urllib.parse import parse_qs

from app import flask_app, Config
from db import (
    DB_Account,
    DB_Event,
)

@flask_app.route('/edit/savings', methods=['POST'])
def edit_savings():
    Config.MONGO[Config.DB]
    # incoming values
    data = parse_qs( request.get_data(as_text=True) )
    data = {k:data[k][0] for k in data}
    data['rate'] = float(data['rate'])
    data['value'] = float(data['amount'])
    data['name'] = data['account_name']
    # get existing object
    acct = DB_Account.objects(name=data['name'])[0]
    for key in acct:
        try:
            if acct[key] != data[key]:
                acct.update(**{key:data[key]})
        except KeyError: continue
    out = {'finish': data['finish'] == 'finish'}
    return jsonify(out)

@flask_app.route('/edit/loan', methods=['POST'])
def edit_loan():
    Config.MONGO[Config.DB]
    # incoming values
    data = parse_qs( request.get_data(as_text=True) )
    data = {k:data[k][0] for k in data}
    data['rate'] = float(data['rate'])
    data['length'] = int(data['length'])
    data['value'] = float(data['principle'])
    data['name'] = data['account_name']
    # get existing object
    acct = DB_Account.objects(name=data['name'])[0]
    for key in acct:
        try:
            if acct[key] != data[key]:
                acct.update(**{key:data[key]})
        except KeyError: continue
    out = {'finish': data['finish'] == 'finish'}
    return jsonify(out)

@flask_app.route('/edit/event', methods=['POST'])
def edit_event():
    Config.MONGO[Config.DB]
    # incoming values
    data = parse_qs( request.get_data(as_text=True) )
    obj_dict = {
        'credit': {
            'account': [],
            'amount': [],
        },
        'debit': {
            'account': [],
            'amount': [],
        },
    }
    for key in data:
        try:
            accts, idx, var_type = key.split('-')
            acct_type = accts.split('_')[0]
            data_val = DB_Account.objects(name=data[key][0])[0] \
                        if var_type == 'account' else float(data[key][0])
            obj_dict[acct_type][var_type].insert(int(idx), data_val)
        except ValueError: continue
    data_dict = {}
    for acct_type in obj_dict:
        for var_type in obj_dict[acct_type]:
            data_dict[f'{acct_type}_{var_type}s'] = obj_dict[acct_type][var_type]
    # get existing object
    event = DB_Event.objects(name=data['name'][0])[0]
    for key in event:
        try:    
            if event[key] != data_dict[key]:
                event.update(**{key: data_dict[key]})
        except KeyError: continue
    out = {'finish': data['finish'][0] == 'finish'}
    return jsonify(out)