from datetime import date
from flask import (
    render_template,
    request,
)

from app import flask_app, Config
from app.forms import ScheduleForm
from db import (
    DB_Event,
    DB_Scheduler,
)

@flask_app.route('/schedule', methods=['GET','POST'])
def schedule():
    Config.MONGO[Config.DB]
    title = 'Schedule Event'
    form = ScheduleForm()
    event_list = DB_Event.objects()
    event_names = [e.name for e in event_list]
    # event_list = list(events.keys())
    form.event.choices = event_names
    if form.submit() and request.method == 'POST':
        name = form.event.data
        print(form.data)
        event = DB_Event.objects(name=name)[0] # names are unique
        start = form.start_date.data
        freq = form.frequency.data
        units = form.frequency_units.data
        DB_Scheduler(
            name=name,
            event=event,
            start=start,
            freq=freq,
            units=units,
        ).save()
    return render_template('schedule.html', title=title, form=form)
