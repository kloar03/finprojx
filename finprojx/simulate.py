import numpy as np
import pandas as pd
import xarray as xr
import datetime
import time
import warnings
from utils.scheduler import Scheduler
from utils.accounts import Loan, Savings
from utils.time_utils import (
    calculate_day,
    generate_days,
    number_of_days_in_year,
    is_payday
)
event_manager = Scheduler(2085)
main_s = Savings('AmeriCU', amount=9000, rate=.01)
house_l = Loan(name='House', principle=176130, rate=.03625, length=30)

start = time.time()
# accounts = {
#     main_s.name:        main_s,
# }
# debts = {
#     house_l.name:       house_l,
# }
accounts = {
    main_s.name:        main_s,
    house_l.name:       house_l,
}

event_manager.add_event(
    'K_payday',
    lambda: main_s.make_deposit(2350.00),
    datetime.date(2020, 1, 3),
    'every other week'
)
event_manager.add_event(
    f'{house_l.name}_charge',
    lambda: main_s.make_withdrawal(house_l.minimum+536.76),
    datetime.date(2020, 2, 1),
    'every month'
)
event_manager.add_event(
    f'{house_l.name}_payment',
    lambda: house_l.make_payment(house_l.minimum),
    datetime.date(2020, 2, 1),
    'every month'
)
# pay = {
#     main_s.name:        2350.00,
# }
# expense = {
#     main_s.name:        house_l.minimum+536.76,
#     house_l.name:       house_l.minimum,
# }

# payday_gen = is_payday()
for year in range(2020, 2080):
    num_days = number_of_days_in_year(year)
    # year_rates = {k:rates[k]/num_days for k in rates}
    # TODO: handle leap years wrt interest rates
    # for day in generate_days(year):
    #     next(payday_gen) # prepare the generator
    #     payday_today = payday_gen.send(day) # update with current day
    #     bills_today = day.day == 1
    #     income = pay if payday_today else {}
    #     payments = {} if not bills_today else expense
    #     calculate_day(savings=accounts,
    #                 debts=debts,
    #                 # rates=year_rates,
    #                 income=income,
    #                 payments=payments,
    #                 number_of_days_in_year=num_days)
    for day in generate_days(year):
        # if day in event_manager.events:
        #     names = event_manager.events[day]
        #     for name in names:
        #         print(event_manager.func_map[name])
        for event in event_manager[day]:
            event() # perform the event
        for account in accounts.values():
            account.apply_interest(interest_units='days',
                                    number_of_days=num_days)


# print(accounts)
# print(debts)
for name in accounts:
    print(accounts[name])
end = time.time()
print(end-start)
