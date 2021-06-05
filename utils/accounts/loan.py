import numpy as np
import pandas as pd
import xarray as xr
import datetime
import time
import warnings
from .account import Account
from ..misc import float_as_money

class Loan(Account):
    """ class to represent and manage a loan """
    def __init__(self, name: str, principle: float,
                rate: float, length: int, rate_units: str='years'):
        """ class for managing a loan """
        super().__init__(name, rate, rate_units)
        self.principle = principle
        self.length = length

        # get monthly rate for amortization
        rate = self.rate if self.rate_units == 'months' else self.rate/12
        # if length is in years convert to months for amortization calculation
        length = self.length * 12 if self.rate_units == 'years' else self.length
        # amortization calculation
        minimum = self.principle * rate * (1+rate)**length / ( (1+rate)**length - 1 )
        self.minimum = round(minimum, 2)
        self._origination = self.principle
    
    def __repr__(self):
        """ returns the string representation of the class """
        return f"Loan(name={self.name}, origination={float_as_money(self.origination)}, principal={float_as_money(self.principle)}, length={self.length} {self.rate_units})"

    def get_origination(self):
        """ get the origination value of the loan """
        return self._origination
    # disallow changes to the origination value
    origination = property(fget=get_origination)

    def debit(self, value=None) -> float:
        """ method to make payments on the loan, returning any leftover """
        value = value if value else self.minimum
        if value < self.minimum: warnings.warn('Failed to make the minimum payment on {self.name}')
        if self.principle < value:
            amount = self.principle
            leftover = value-self.principle
        else: # no leftover remaining
            amount = value
            leftover = 0.0
        self.principle -= amount
        return round(leftover, 2)
    
    def is_complete(self):
        return self.principle <= 0.0
# l = Loan(name='House', principle=176130, rate=.03625, length=30)
# print(isinstance(l, Account))
# print(l.principle)
# l.make_payment()
# print(l.principle)
# l.apply_interest()
# print(l.principle)
