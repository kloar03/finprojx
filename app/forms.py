from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SubmitField
from wtforms.validators import DataRequired

class AddEventForm(FlaskForm):
    date = DateField('Event Date', validators=[DataRequired()])
    frequency = StringField('Event Frequency', validators=[DataRequired()])
    submit = SubmitField('Add Event')