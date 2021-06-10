from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app import flask_app, Config
from app.forms import AddAccountForm
from db import DB_Account

@flask_app.route('/add/account', methods=['GET','POST'])
def add_account():
    Config.MONGO[Config.DB]
    form = AddAccountForm()
    title = 'Add Account'
    if form.submit() and request.method == 'POST':
        if add_account_main(form):
            red_to = '/' if form.data['submit'] else url_for('add_account')
            return redirect(red_to)
    return render_template('add_account.html', title=title, form=form)

def out_of_range(number, low, high):
    """ check if a number outside a given range """
    return (low > number) or (high < number)

def add_account_main(form) -> bool:
    """
    the main functionality for adding new accounts
    """
    # make sure we have a valid type
    acct_type = form.data['account_type'] 
    if acct_type not in ['Savings', 'Loan']:
        flash('Please select an account type!', category='error')
    
    # make sure we have a valid name and rate in either case
    name = form.data['account_name']
    if not name:
        flash('Enter an account name', category='error')
    rate = form.data['rate']
    if not rate or out_of_range(rate, 0, 100):
        flash('Enter a rate as a decimal (between 0-100)', category='error')
        return False

    # savings logic
    if acct_type == 'Savings':
        value = form.data['amount']
        length = None
        if not value:
            flash('Must enter an amount for a savings account', category='error')
            return False
        
    # loan logic
    if acct_type == 'Loan':
        value = form.data['principle']
        length = form.data['length']
        if (not value) or (not length):
            flash('Must enter principle and length for loan account')
            return False
    # collect the account info and return
    DB_Account(
        name=name,
        type=form.account_type.data,
        value=value,
        rate=rate,
        length=length, 
    ).save()
    return True