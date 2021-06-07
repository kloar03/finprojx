from datetime import date
from flask import (
    redirect,
    render_template,
    request,
    url_for,
)

from app import flask_app
from app.forms import SimulateForm
from db.nosql_account import NoSQL_Account
from utils.accounts import Savings, Loan
from utils.event import Event
from utils.scheduler import Scheduler
from utils.time_utils import (
    generate_days,
    number_of_days_in_year,
)

accounts = {
    'AmeriCU': Savings('AmeriCU', 10000, .0025),
    'Mortgage_1': Loan('Mortgage_1', 178000, .03625, 30),
}
events = {
    'Mortgage_1_Pay': Event(credit_dict={accounts['AmeriCU']:811.77},
                           debit_dict={accounts['Mortgage_1']:811.77}),
    'Paycheck': Event(debit_dict={accounts['AmeriCU']:2600})
}

event_arg_lists = [
    ['Mortgage_1_Pay',events['Mortgage_1_Pay'], date(2021,6,14), 'every month'],
    ['Paycheck',events['Paycheck'], date(2021,6,19), 'every month'],
]


@flask_app.route('/simulate', methods=['GET','POST'])
def simulate():
    title = 'Simulate'
    form = SimulateForm()
    if form.submit() and request.method == 'POST':
        seq_name = 'original'
        cur_year = date.today().year
        num_years = form.sim_years.data
        fin_year = cur_year + num_years
        event_manager = Scheduler(fin_year)
        for event_args in event_arg_lists:
            event_manager.add_event(*event_args)
        docs = []
        for year in range(cur_year, fin_year):
            num_days = number_of_days_in_year(year)
            for day in generate_days(year):
                for event in event_manager[day]:
                    event()
                for account in accounts.values():
                    account.apply_interest(interest_units='days',
                                            number_of_days=num_days)
                    try:
                        value = account.principle
                    except AttributeError:
                        value = account.amount

                    doc = NoSQL_Account(
                        sim_id=seq_name,
                        account_type=type(account).__name__,
                        account_name=account.name,
                        year=day.year,
                        month=day.month,
                        day=day.day,
                        value=value,
                        rate=account.rate
                    )
                    docs.append(doc)
            NoSQL_Account.objects.insert(docs)
            docs = []
        return redirect(url_for('view'))
    return render_template('simulate.html', title=title, form=form)
