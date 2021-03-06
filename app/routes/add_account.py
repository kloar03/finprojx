from flask import (
    jsonify,
    render_template,
    Response,
    request,
)
from mongoengine.errors import ValidationError
from urllib.parse import parse_qs

from app import flask_app, Config
from app.forms import (
    AddSavingsForm,
    AddLoanForm,
)
from db import DB_Account

@flask_app.route('/add/savings', methods=['POST'])
def add_savings():
    Config.MONGO[Config.DB]
    data = request.get_data(as_text=True)
    form = AddSavingsForm()
    if form.submit():
        success = add_account_main(form, 'Savings')
        data = parse_qs( data )
        out = {'finish': (data['finish'] == 'finish') or (not success)}
        return jsonify(out)
    return Response({}, status=406, mimetype='application/json')

@flask_app.route('/add/loan', methods=['POST'])
def add_loan():
    Config.MONGO[Config.DB]
    data = request.get_data(as_text=True)
    form = AddLoanForm()
    if form.submit():
        success = add_account_main(form, 'Loan')
        data = parse_qs(data)
        out = {'finish': (data['finish'] == 'finish') or (not success)}
        return jsonify(out)
    return Response({}, status=406, mimetype='application/json')

@flask_app.route('/add/account', methods=['GET','POST'])
def add_account():
    Config.MONGO[Config.DB]
    data = request.get_data()
    sForm = AddSavingsForm()
    lForm = AddLoanForm()
    title = 'Add Account'
    if (sForm.submit() or lForm.submit()) and request.method == 'POST':
        if sForm.submit():
            form = sForm
            account_type = 'Savings'
        else:
            form = lForm
            account_type = 'Loan'
        add_account_main(form, account_type)
        data = data.decode()        
        data = [kv.split('=') for kv in data.split('&')]
        data = {k:v for (k, v) in data}
        out = {'finish': data['finish'] == 'finish'}
        return jsonify(out)
    return render_template('add_account.html', title=title)#, form=form)


def out_of_range(number, low, high):
    """ check if a number outside a given range """
    return (low > number) or (high < number)

def add_account_main(form, acct_type=None) -> bool:
    """
    the main functionality for adding new accounts
    """
    # make sure we have a valid type
    if acct_type is None:
        try:
            acct_type = form.data['account_type'] 
            if acct_type not in ['Savings', 'Loan']:
                return False
        except KeyError:
            print('expected "account_type" key but it was not present...')
    # make sure we have a valid name and rate in either case
    name = form.data['account_name']
    if not name:
        return False
    rate = form.data['rate']
    if not rate or out_of_range(rate, 0, 100):
        return False

    # savings logic
    if acct_type == 'Savings':
        value = form.data['amount']
        length = None
        if value is None:
            return False
        
    # loan logic
    if acct_type == 'Loan':
        value = form.data['principle']
        length = form.data['length']
        if (not value) or (not length):
            return False
    # collect the account info and return
    try:
        DB_Account(
            name=name,
            type=acct_type,
            value=value,
            rate=rate,
            length=length, 
        ).save()
    except ValidationError:
        return False
    return True