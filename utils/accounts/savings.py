import numpy as np
import pandas as pd
import xarray as xr
import datetime
import time
import warnings
from .account import Account
from ..misc import float_as_money

class Savings(Account):
    """ class to represent and manage a savings account """
    def __init__(self, name: str, amount: float,
                rate: float, rate_units: str='years'):
        """ class for managing a loan """
        super().__init__(name, rate, rate_units)
        self.amount = amount
    
    def __repr__(self):
        """ returns the string representation of the class """
        return f"Savings(name={self.name}, amount={float_as_money(self.amount)}, rate={self.rate} per {self.rate_units[:-1]})"


    def debit(self, amount=0.00) -> None:
        """ method to deposit into savings account """
        if amount <= 0.00: raise ValueError(f'must make strictly positive deposit, tried {amount}')
        self.amount += amount
    
    def credit(self, amount=0.00) -> float:
        """ method to withdrawal from savings account """
        if amount <= 0.00: 
            raise ValueError(f'must make strictly positive deposit, tried {amount}')
        if amount > self.amount: 
            raise ValueError(f"attempted to overdraw account, had {self.amount:.2f} but withdrew {amount:.2f}")
        self.amount -= amount
        return amount

# s = Savings(name='AmeriCU', amount=9000, rate=.01)
# print(s.amount)
# s.make_deposit(1000)
# print(s.amount)
# s.make_withdrawal(500)
# print(s.amount)
# s.apply_interest()
# print(s.amount)
