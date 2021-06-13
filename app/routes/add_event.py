from flask import (
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from app import flask_app, Config
from app.forms import AddEventForm
from db import (
    DB_Account,
    DB_Event,
)

@flask_app.route('/add/event', methods=['GET','POST'])
def add_event():
    Config.MONGO[Config.DB]
    form = AddEventForm()
    # populate the choices w/ current accounts
    set_account_choices(form.credit_accounts)
    set_account_choices(form.debit_accounts)
    cur_accounts = DB_Account.objects()
    title = 'Add Event'
    if request.method == 'POST' and form.add_credit.data: # POST
        form.credit_accounts.append_entry()
        form.credit_accounts.entries[-1].account.choices = cur_accounts
        return render_template('add_event.html', title=title, form=form)
    elif request.method == 'POST' and form.add_debit.data:
        form.debit_accounts.append_entry()
        form.debit_accounts.entries[-1].account.choices = cur_accounts
    elif request.method == 'POST' and form.submit(): # an actual submission
        url = url_for('add_event') if form.more.data else '/'
        if add_event_main(form):
            return redirect(url)
    # elif form.submit() and form.submit.data: # an actual submission
    #     try:
    #         event = add_event_main(form)
    #     except:
    #         ...
    #     finally:
    #        return redirect('/')
        
    return render_template('add_event.html', title=title, form=form)

def set_account_choices(accounts) -> None:
    """ sets list of choices from DB accounts """
    cur_accounts = DB_Account.objects()
    for entry in accounts.entries:
        entry.account.choices = [acct.name for acct in cur_accounts]

def add_event_main(form) -> bool:
    """
    the main functionality for adding new events
    """
    # parse accounts: unused accounts group results in {'amount':None, ...}
    credit_accounts = [acct.data for acct in form.credit_accounts
                       if acct['amount'].data]
    debit_accounts = [acct.data for acct in form.debit_accounts
                      if acct['amount'].data]
    # transactions should be equal quantities
    if credit_accounts and debit_accounts:
        cred_sum = sum([acct['amount'] for acct in credit_accounts])
        deb_sum = sum([acct['amount'] for acct in debit_accounts])
        if cred_sum != deb_sum:
            flash('The total amount transferred should equal funds provided, '
                 f'but you transferred {deb_sum} while supplying {cred_sum}',
                 category='error')
            return False
    # get our credit account objects
    acct_names = [a['account'] for a in credit_accounts]
    c_amounts = [a['amount'] for a in credit_accounts]
    c_accounts = DB_Account.objects(name__in=acct_names)
    # TODO: pay ahead (extra payments) for loans
    # TODO: ensure minimum payment
    acct_names = [a['account'] for a in debit_accounts]
    d_amounts = [a['amount'] for a in debit_accounts]
    d_accounts = DB_Account.objects(name__in=acct_names)
    # # define how and what we debit, plus check for loan minimums
    # to_flash = []
    # debit_accounts = []
    # debit_amounts = []
    # for acct in form.debit_accounts.data:
    #     acc_name = acct['name']
    #     account = DB_Account.objects(name=acc_name)[0] # only one return
    #     amount = acct['amount']
    #     is_loan = account.type == 'Loan'
    #     if is_loan and amount < account.minimum: # payment too small
    #         to_flash.append(f'Attempted payment of {amount} to loan '
    #                         f'{account.name} but minimum is {account.minimum}.')
    #     deb_actions[account] = amount
    # if to_flash: # found an error
    #     flash('\n'.join(to_flash), category='error')
    #     return {}

    # TODO: ajax validation
    # perform manual validation
    if not form.name.data:
        flash('Must pass a name!', category='error')
        return False

    DB_Event(
        name=form.name.data,
        credit_accounts=c_accounts,
        credit_amounts=c_amounts,
        debit_accounts=d_accounts,
        debit_amounts=d_amounts,
    ).save()
    return True