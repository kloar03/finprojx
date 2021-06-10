from mongoengine import (
    Document,
    DateField,
    StringField,
    ReferenceField,
)

from .DB_Event import DB_Event

class DB_Scheduler(Document):
    name = StringField(required=True, max_length=50,
                       primary_key=True, unique=True)
    event = ReferenceField(DB_Event, required=True)
    start = DateField(required=True)
    freq = StringField(required=True)
    units = StringField(required=True)