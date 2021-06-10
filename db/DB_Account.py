from mongoengine import (
    Document,
    FloatField,
    IntField,
    StringField,
)
from mongoengine.fields import IntField

class DB_Account(Document):
    name = StringField(required=True, max_length=50,
                       primary_key=True, unique=True)
    type = StringField(required=True, choices=['Savings', 'Loan'])
    
    value = FloatField(required=True, min_value=.0)
    rate = FloatField(required=True, min_value=.0)
    length = IntField(min_value=0)