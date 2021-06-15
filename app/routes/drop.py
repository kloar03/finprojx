from flask import (
    flash,
    render_template
)
from mongoengine import connect

from app import flask_app, Config
from app.forms import DropCollectionsForm
from db import (
    DB_Account,
    DB_Event,
    DB_Scheduler,
    DB_Simulate
)

@flask_app.route('/drop', methods=['GET', 'POST'])
def drop():
    Config.MONGO[Config.DB]
    title = 'Drop Form'
    form = DropCollectionsForm()
    if form.validate_on_submit(): # POST
        if form.accounts.data:
            try:
                DB_Account.objects().delete()
            except AttributeError:
                ...
            flash('Accounts Dropped')
        elif form.events.data:
            try:
                DB_Event.objects().delete()
            except AttributeError:
                ...
            flash('Events Dropped')
        elif form.schedules.data:
            try:
                DB_Scheduler.objects().delete()
            except AttributeError:
                ...
            flash('Schedules Dropped')
        elif form.simulation.data:
            try:
                DB_Simulate.objects().delete()
            except AttributeError:
                ...
            flash('Simulation Dropped')
    return render_template('drop.html', title=title, form=form)
