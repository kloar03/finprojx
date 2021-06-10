from typing import List
from mongoengine import (
    Document,
    FloatField,
    ListField,
    StringField,
    ReferenceField,
)
from .DB_Account import DB_Account

class DB_Event(Document):
    name = StringField(required=True, max_length=50,
                       primary_key=True, unique=True)
    credit_accounts = ListField(ReferenceField(DB_Account))
    debit_accounts = ListField(ReferenceField(DB_Account))
    credit_amounts = ListField(FloatField())
    debit_amounts = ListField(FloatField())