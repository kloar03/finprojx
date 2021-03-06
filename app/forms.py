from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, FieldList, FormField
from wtforms.fields.core import Field
from wtforms.fields.html5 import DateField, IntegerField, IntegerRangeField, DecimalField
from wtforms.validators import DataRequired, NumberRange

class SimulateForm(FlaskForm):
    sim_years = IntegerField('Number of years to simulate', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit')

class ScheduleForm(FlaskForm):
    event = SelectField('Event to Schedule', validators=[DataRequired()])
    start_date = DateField('Start Date')
    frequency = SelectField('Event Frequency',
                           validators=[DataRequired()],
                           choices=[
                               'once',
                               'every',
                               'every other',
                               'every third',
                               'every fourth',
                           ])
    frequency_units = SelectField('Frequency Units',
                                 validators=[DataRequired()],
                                 choices=[
                                     'days',
                                     'weeks',
                                     'months',
                                     'years'
                                 ])
    submit = SubmitField('Submit')

class EventSubForm(FlaskForm):
    class Meta:
        csrf = False
    account = SelectField('Account', validators=[DataRequired()])
    amount = DecimalField('Amount', validators=[NumberRange(min=.0), DataRequired()])

class AddEventForm(FlaskForm):
    name = StringField('Event Name')
    credit_accounts = FieldList(FormField(EventSubForm), min_entries=1)
    add_credit = SubmitField('Add Another')
    debit_accounts = FieldList(FormField(EventSubForm), min_entries=1)
    add_debit = SubmitField('Add Another')
    more = SubmitField('Continue Creating Events')
    submit = SubmitField('Finish Creating Events')

class AddSavingsForm(FlaskForm):
    # TODO: conditional validation
    account_name = StringField('Account Name', validators=[DataRequired()])
    rate = DecimalField('Rate')
    amount = DecimalField('Amount')
    more = SubmitField('Continue Creating Accounts')
    submit = SubmitField('Finish Creating Accounts')

class AddLoanForm(FlaskForm):
    # TODO: conditional validation
    account_name = StringField('Account Name', validators=[DataRequired()])
    rate = DecimalField('Rate')
    principle = DecimalField('Loan Principle')
    length = IntegerField('Loan Length')
    more = SubmitField('Continue Creating Accounts')
    submit = SubmitField('Finish Creating Accounts')

class DropCollectionsForm(FlaskForm):
    accounts = SubmitField('Drop Accounts')
    events = SubmitField('Drop Events')
    schedules = SubmitField('Drop Schedules')
    simulation = SubmitField('Drop Simulation')
