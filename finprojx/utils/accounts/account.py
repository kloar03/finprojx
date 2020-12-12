import datetime
import warnings

class Account:
    """ class to represent and manage an account """
    def __init__(self, name: str, rate: float, rate_units: str='years'):
        """ class for managing an account """
        self.name = name
        self.rate = rate
        self.rate_units = self.resolve_units(rate_units)
    
    def __repr__(self):
        """ returns the string representation of the class """
        return f"Account(name={self.name}, rate={self.rate} per {self.rate_units[:-1]})"
    
    def apply_interest(self, **kwargs) -> None:
        """ apply interest to the account value for the units passed """
        if type(self) == Account: raise NotImplementedError
        interest_units = kwargs.get("interest_units", self.rate_units)
        number_of_days = kwargs.get("number_of_days", 365)
        interest_units = self.resolve_units(interest_units) # limit the possible values to work with
        if interest_units == self.rate_units:
            try:
                self.principle *= (1 + self.rate)
            except AttributeError:
                self.amount *= (1 + self.rate)
            return None
        # convert interest units to years
        if interest_units == 'years':
            interest_units_coef = 1
        elif interest_units == 'months':
            interest_units_coef = 12
        else: # days
            interest_units_coef = number_of_days
        # convert account rate units to years
        if self.rate_units == 'years':
            account_units_coef = 1
        elif self.rate_units == 'months':
            account_units_coef = 12
        else: # days
            account_units_coef = number_of_days
        rate = account_units_coef * self.rate / interest_units_coef
        try:
            self.principle *= (1 + rate)
        except AttributeError:
            self.amount *= (1 + rate)
            
    @staticmethod
    def resolve_units(units):
        if units in ['y', 'year', 'years']:
            return 'years'
        elif units in ['m', 'month', 'months']:
            return 'months'
        elif units in ['d', 'day', 'days']:
            return 'days'
        else:
            raise ValueError(f'unable to resolve {units}')




