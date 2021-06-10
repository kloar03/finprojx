from mongoengine import (
    Document,
    DateField,
    FloatField,
    StringField,
    ReferenceField,
)

from .DB_Account import DB_Account

class DB_Simulate(Document):
    name = StringField(required=True, max_length=50)
    account = ReferenceField(DB_Account, required=True)
    date = DateField(required=True)
    amount = FloatField(required=True)