import numpy as np
import pandas as pd
import xarray as xr
import datetime
import time
import warnings
from utils.scheduler import Scheduler
from utils.accounts import Loan, Savings
from utils.event import Event
from utils.time_utils import (
    calculate_day,
    generate_days,
    number_of_days_in_year,
    is_payday
)
# database operations
from mongoengine import connect
from db.nosql_account import NoSQL_Account
from db import DB_Account

mongo_client = connect('simulation_save', host='localhost', port=27017)
db = mongo_client['finprojx']

event_manager = Scheduler(2085)
main_s = Savings('AmeriCU', amount=9000, rate=.01)
invest_s = Savings('401k', amount=23500, rate=.06)
house_l = Loan(name='House', principle=176130, rate=.03625, length=30)
car1_l = Loan(name='Car1', principle=10000, rate=.05, length=5)

start = time.time()
accounts = [
    main_s,
    invest_s,
    house_l,
    car1_l,
]
for account in accounts:
    try:
        value = account.amount
    except:
        value = account.origination
    DB_Account(
        name=account.name,
        type=account.__class__.__name__,
        value=value,
        rate=account.rate,
    ).save()
exit()

contrib_401k = Event(
    credit_dict={
        main_s: 150
    },
    debit_dict={
        invest_s: 150
    }
)

mortgage = Event(
    credit_dict={
        main_s: house_l.minimum+536.76
    },
    debit_dict={
        house_l: house_l.minimum
    },
    stop_cond=house_l.is_complete
)

cost_of_living = Event(
    credit_dict={
        main_s: 2500/15
    }
)

car1_down = Event(
    credit_dict={
        main_s: 5000
    }
)

car1 = Event(
    credit_dict={
        main_s: car1_l.minimum
    },
    debit_dict={
        car1_l: car1_l.minimum
    },
    stop_cond=car1_l.is_complete
)

event_manager.add_event(
    'K_payday',
    lambda: main_s.debit(2350.00),
    datetime.date(2020, 1, 3),
    'every other week'
)
event_manager.add_event(
    'K_work_contrib',
    lambda: invest_s.debit(215.00),
    datetime.date(2020, 1, 10),
    'every other week'
)
event_manager.add_event(
    'K_my_contrib',
    contrib_401k,
    datetime.date(2020, 1 , 3),
    'every other week'
)
event_manager.add_event(
    'regular_spending',
    cost_of_living,
    datetime.date(2020,1,1),
    'every other day'
)
event_manager.add_event(
    f'{house_l.name}',
    mortgage,
    datetime.date(2020, 2, 1),
    'every month'
)

event_manager.add_event(
    f'car1_down',
    car1_down,
    datetime.date(2021, 6, 1),
    'once'
)

event_manager.add_event(
    car1_l.name,
    car1,
    datetime.date(2021, 6, 1),
    'every month'
)

seq_name = 'regular'
docs = []
for year in range(2020, 2080):
    num_days = number_of_days_in_year(year)
    for day in generate_days(year):
        for event in event_manager[day]:
            event() # perform the event
        for account in accounts.values():
            account.apply_interest(interest_units='days',
                                    number_of_days=num_days)
            try:
                value = account.principle
            except AttributeError:
                value = account.amount

            doc = NoSQL_Account(
                sim_id=seq_name,
                account_type=type(account).__name__,
                account_name=account.name,
                year=day.year,
                month=day.month,
                day=day.day,
                value=value,
                rate=account.rate
            )
            docs.append(doc)
    NoSQL_Account.objects.insert(docs)
    docs = []

for name in accounts:
    print(accounts[name])
end = time.time()
print(end-start)
# NoSQL_Account.drop_collection()
db.drop_collection('finprojx')