from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField
from wtforms.fields.html5 import DateField, IntegerField, IntegerRangeField, DecimalField
from wtforms.validators import DataRequired

class AddEventForm(FlaskForm):
    date = DateField('Event Date', validators=[DataRequired()], format='%Y-%m-%d')
    frequency = StringField('Event Frequency', validators=[DataRequired()])
    submit = SubmitField('Add Event')

class AddAccountForm(FlaskForm):
    # TODO: conditional validation
    # account_type = SelectField('Account Type',
    account_type = RadioField('Account Type',
                    choices=[('savings','Savings'),('loan','Loan')],
                    validators=[DataRequired()])
    rate = IntegerField('Rate')
    amount = DecimalField('Amount')
    principle = DecimalField('Loan Principle')
    length = IntegerField('Loan Length')
    submit = SubmitField('Create Account')

class DropCollectionsForm(FlaskForm):
    submit = SubmitField('Drop Collections')