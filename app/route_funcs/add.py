from flask import flash
from utils.accounts import Loan, Savings

def out_of_range(number, low, high):
    """ check if a number outside a given range """
    return (low > number) or (high < number)

def add_event_main() -> None:
    ...

def add_account_main(form) -> dict:
    """
    the main functionality for adding new accounts
    """
    # make sure we have a valid type
    if form.data['account_type'] not in ['savings', 'loan']:
        flash('Please select an account type!', category='error')
    
    # make sure we have a valid name and rate in either case
    name = form.data['account_name']
    if not name:
        flash('Enter an account name', category='error')
    rate = form.data['rate']
    if not rate or out_of_range(rate, 0, 100):
        flash('Enter a rate as a percentile (between 0-100)', category='error')
    
    # savings logic
    if form.data['account_type'] == 'savings':
        amount = form.data['amount']
        if not amount:
            flash('Must enter an amount for a savings account', category='error')
            return {}
        return {name: Savings(name=name, amount=amount, rate=rate)}
        
    # loan logic
    if form.data['account_type'] == 'loan':
        principle = form.data['principle']
        loan_length = form.data['length']
        if (not principle) or (not loan_length):
            flash('Must enter principle and length for loan account')
            return {}
        return {name: Loan(name=name, principle=principle,
                           rate=rate, length=loan_length)}