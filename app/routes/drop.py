from flask import (
    flash,
    render_template
)
from mongoengine import connect

from app import flask_app
from app.forms import DropCollectionsForm
from db.nosql_account import NoSQL_Account

mongo_client = connect('finprojx_app', host='localhost', port=27017)
db = mongo_client['finprojx']

@flask_app.route('/drop', methods=['GET', 'POST'])
def drop():
    title = 'Drop Form'
    form = DropCollectionsForm()
    if form.validate_on_submit(): # POST
        NoSQL_Account.drop_collection()
        db.drop_collection('finprojx_app')
        flash('Collection Dropped')
    return render_template('drop.html', title=title, form=form)
