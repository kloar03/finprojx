from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, RadioField, FieldList, FormField
from wtforms.fields.core import Field
from wtforms.fields.html5 import DateField, IntegerField, IntegerRangeField, DecimalField
from wtforms.validators import DataRequired, NumberRange

class EventSubForm(FlaskForm):
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

class AddAccountForm(FlaskForm):
    # TODO: conditional validation
    # account_type = SelectField('Account Type',
    account_name = StringField('Account Name', validators=[DataRequired()])
    account_type = RadioField('Account Type',
                    choices=[('savings','Savings'),('loan','Loan')],
                    validators=[DataRequired()])
    rate = DecimalField('Rate')
    amount = DecimalField('Amount')
    principle = DecimalField('Loan Principle')
    length = IntegerField('Loan Length')
    more = SubmitField('Continue Creating Accounts')
    submit = SubmitField('Finish Creating Accounts')

class DropCollectionsForm(FlaskForm):
    submit = SubmitField('Drop Collections')