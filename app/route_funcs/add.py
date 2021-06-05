from flask import flash
from numpy.lib.arraysetops import isin
from utils.event import Event
from utils.accounts import Loan, Savings
from pprint import PrettyPrinter

pp = PrettyPrinter(indent=2)

def out_of_range(number, low, high):
    """ check if a number outside a given range """
    return (low > number) or (high < number)

def add_event_main(form, accounts) -> dict:
    """
    the main functionality for adding new events
    """
    pp.pprint(form.data)
    
    # transactions should be equal quantities
    if form.credit_accounts and form.debit_accounts:
        cred_sum = sum([acct['amount'].data for acct in form.credit_accounts])
        deb_sum = sum([acct['amount'].data for acct in form.debit_accounts])
        if cred_sum != deb_sum:
            flash('The total amount transferred should equal funds provided, '
                 f'but you transferred {deb_sum} while supplying {cred_sum}',
                 category='error')
            return {}
    # define what we credit
    cred_actions = {}
    for acct in form.credit_accounts:
        account = accounts[acct['account'].data]
        amount = acct['amount'].data
        cred_actions[account] = amount
    # TODO: pay ahead for loans
    # define how and what we debit, plus check for loan minimums
    to_flash = []
    deb_actions = {}
    for acct in form.debit_accounts:
        account = accounts[acct['account'].data]
        amount = acct['amount'].data
        is_loan = isinstance(account, Loan)
        if is_loan and amount < account.minimum: # payment too small
            to_flash.append(f'Attempted payment of {amount} to loan '
                            f'{account.name} but minimum is {account.minimum}.')
        deb_actions[account] = amount
    if to_flash: # found an error
        flash('\n'.join(to_flash), category='error')
        return {}

    # TODO: ajax validation
    # perform manual validation
    if not form.name.data:
        flash('Must pass a name!', category='error')
        return {}

    e = Event(credit_dict=cred_actions, debit_dict=deb_actions)
    return {form.name.data: e}

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