from mongoengine import Document
from mongoengine import (
    IntField,
    FloatField,
    StringField,
)

class NoSQL_Account(Document):
    sim_id =        StringField(required=True, max_length=30)
    account_type =  StringField(required=True, max_length=25)
    account_name =  StringField(required=True, max_length=25)
    year =          IntField(required=True)
    month =         IntField(required=True)
    day =           IntField(required=True)
    value =         FloatField(required=True)
    rate =          FloatField(required=True)