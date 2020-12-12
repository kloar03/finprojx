import numpy as np
import pandas as pd
import xarray as xr
import datetime
import time
import warnings

def number_of_days_in_year(year):
    """ return the number of days in the provided year """
    y1 = datetime.date(year, 1,1)
    y2 = datetime.date(year+1, 1,1)
    return (y2-y1).days # days from datetime.timedelta

def generate_days(year):
    """ generator for days in the provided year """
    current_day = datetime.date(year, 1, 1)
    last_day = datetime.date(year, 12, 31)
    day_increment = datetime.timedelta(days=1)
    while current_day <= last_day:
        yield current_day
        current_day += day_increment

def calculate_day(**kwargs) -> None:
    """ update all sources for a day """
    savings = kwargs.get('savings', {})
    debts = kwargs.get('debts', {})
    income = kwargs.get('income', {})
    payments = kwargs.get('payments', {})
    number_of_days_in_year = kwargs.get("number_of_days_in_year", 365)

    for key in savings:
        savings[key].apply_interest(interest_units='days', number_of_days=number_of_days_in_year)
        try: savings[key].make_deposit(income[key])
        except KeyError: pass
        try: savings[key].make_withdrawal(payments[key])
        except KeyError: pass
    for key in debts:
        debts[key].apply_interest(interest_units='days', number_of_days=number_of_days_in_year)
        try: debts[key].make_payment(value=payments[key])
        except KeyError: pass

def is_payday(weekday=5):
    """ generator that returns the if the day is payday """
    payweek = False # assume first friday is not payday
    def is_pay_weekday(weekdate):
        return weekdate.isoweekday() == weekday
    while True:
        date = yield # fed this value
        yield payweek and is_pay_weekday(date)
        payweek = payweek if not is_pay_weekday(date) else not payweek
