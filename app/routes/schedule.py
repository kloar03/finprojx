from datetime import date
from flask import (
    render_template,
    request,
)


from app import flask_app
from app.forms import ScheduleForm
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

event_arg_lists = [
    ['Mortgage_1_Pay',events['Mortgage_1_Pay'], date(2021,6,14), 'every month'],
    ['Paycheck',events['Paycheck'], date(2021,6,19), 'every month'],
]

@flask_app.route('/schedule', methods=['GET','POST'])
def schedule():
    title = 'Schedule Event'
    form = ScheduleForm()
    event_list = list(events.keys())
    form.event.choices = event_list
    if form.submit() and request.method == 'POST':
        name = form.event.data
        event = events[name]
        start = form.start_date.data
        freq = form.frequency.data
        units = form.frequency_units.data
        # event_manager.add_event(name, event, start, f'{freq} {units}')
        event_arg_lists.append(
            [name, event, start, f'{freq} {units}']
        )
    return render_template('schedule.html', title=title, form=form)
