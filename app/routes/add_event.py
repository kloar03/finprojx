from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app import flask_app
from app.forms import AddEventForm
from utils.accounts import Savings, Loan
from utils.event import Event

accounts = {
    'AmeriCU': Savings('AmeriCU', 10000, .0025),
    'Mortgage_1': Loan('Mortgage_1', 178000, .03625, 30),
}
events = {
    'Mortgage_1_Pay': Event(credit_dict={accounts['AmeriCU']:811.77},
                           debit_dict={accounts['Mortgage_1']:811.77}),
    'Paycheck': Event(debit_dict={accounts['AmeriCU']:2600})
}

@flask_app.route('/add/event', methods=['GET','POST'])
def add_event():
    form = AddEventForm()
    # populate the choices w/ current accounts
    cur_accounts = list(accounts.keys())
    for entry in form.credit_accounts.entries:
        entry.account.choices = cur_accounts
    for entry in form.debit_accounts.entries:
        entry.account.choices = cur_accounts
    title = 'Add Event'
    if request.method == 'POST' and form.add_credit.data: # POST
        form.credit_accounts.append_entry()
        form.credit_accounts.entries[-1].account.choices = cur_accounts
        return render_template('add_event.html', title=title, form=form)
    elif request.method == 'POST' and form.add_debit.data:
        form.debit_accounts.append_entry()
        form.debit_accounts.entries[-1].account.choices = cur_accounts
    elif form.submit() and form.more.data: # an actual submission
        event = add_event_main(form, accounts)
        for name in event:
            events[name] = event[name]
        if event:
            return redirect(url_for('add_event'))
    elif form.submit() and form.submit.data: # an actual submission
        try:
            event = add_event_main(form, accounts)
            for name in event:
                events[name] = event[name]
        except:
            ...
        finally:
           return redirect('/')
        
    return render_template('add_event.html', title=title, form=form)

def add_event_main(form, accounts) -> dict:
    """
    the main functionality for adding new events
    """
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
